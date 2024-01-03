import logging

from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.v3_pool_abi import PANCAKESWAP_V3_POOL_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.pancakeswap_info import PANCAKESWAP_V3_BSC_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("PancakeSwap V3 State Service")


class PancakeSwapV3Info:
    mapping = {
        Chain.bsc: PANCAKESWAP_V3_BSC_INFO
    }


class PancakeSwapV3Service(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = PancakeSwapV3Info.mapping.get(chain_id)
        self.masterchef_addr = self.pool_info['master_chef_address']
        self.masterchef_abi = self.pool_info['master_chef_abi']
        self.nft_token_manager = self.pool_info['NFT_token_manager']
        self.NFT_abi = self.pool_info['NFT_abi']

    def get_service_info(self):
        info = {
            Dex.pancake_v3: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit: int = 1, supplied_data:dict = None):
        web3 = self.state_service.get_w3()
        self.masterchef_addr = self.checksum_address(web3, self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.poolLength().call()
        rpc_calls = {}
        for pid in range(1, int(pool_length / limit) + 1):
            query_id = f'poolInfo_{pid}_'
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[pid]
            )

        return rpc_calls

    def decode_all_supported_lp_token(self, response_data, supplied_data:dict = None):
        result = {}
        for key, value in response_data.items():
            pid = key.split("_")[1]
            v3_pool = value[1]
            result[v3_pool] = {
                "pid": pid,
                "token0": value[2],
                'token1': value[3],
                'fee': value[4],
                'stakeLiquidity': value[5],
                'stakeBoostLiquidity': value[6]
            }

        return result

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            for fn_name in ["liquidity", "slot0"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}_{self.chain_id}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=PANCAKESWAP_V3_POOL_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)
            query_id = f'getLatestPeriodInfoByPid_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name='getLatestPeriodInfoByPid',
                fn_paras=[int(pid)],
                block_number=block_number)
        return rpc_calls

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        result = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            token0 = value.get("token0")
            token1 = value.get("token1")
            fee = value.get('fee')
            stake_liquidity = value.get('stakeLiquidity')
            stake_boost_liquidity = value.get('stakeBoostLiquidity')
            total_liquidity = response_data.get(f'liquidity_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                                0)
            sqrt_price_x96 = response_data.get(f"slot0_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            price = self.convert_q64_96_to_integer(sqrt_price_x96)
            cake_per_second = response_data.get(f"getLatestPeriodInfoByPid_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            result[lp_token] = {
                "pid": pid,
                "token0": token0,
                'token1': token1,
                'fee': fee,
                'stakeLiquidity': stake_liquidity / 10 ** 18,
                'stakeBoostLiquidity': stake_boost_liquidity / 10 ** 18,
                "totalLiquidity": total_liquidity / 10 ** 18,
                "currentPrice": price,
                "cakePerSecond": cake_per_second / 10 ** 18
            }
        return result

    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for key, value in lp_token_info.items():
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[key],
                        block_number=block_number)
                    rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(
            self, supplied_data, balance_info, block_number: int = "latest"):
        lp_token_balance = {}
        lp_token_info = supplied_data['lp_token_info']
        for key, value in lp_token_info.items():
            lp_token_balance[key] = {}
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    lp_token_balance[key][token] = balance_info.get(query_id) / 10 ** balance_info.get(
                        decimals_query_id)
        result = self.calculate_lp_token_price_info(lp_token_info, lp_token_balance)
        return result

    def calculate_lp_token_price_info(
            self, lp_token_info, lp_token_balance):
        for lp_token, value in lp_token_info.items():
            token0 = value.get("token0", None)
            token1 = value.get("token1", None)
            if token0 and token1:
                total_liquidity = value.get("totalLiquidity")
                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                lp_token_stake_amount = value.get("stakeLiquidity", 0)
                lp_token_info[lp_token].update({
                    "totalLiquidity": total_liquidity,
                    "stakeLiquidity": lp_token_stake_amount,
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1
                })

                # if token0 and token1:
                #     token0_price = token_price.get(token0)
                #     token1_price = token_price.get(token1)
                #     new_amount1 = balance_of_token1
                #     # if token0_price != 0 and token1_price != 0:
                #     total_of_token0 = balance_of_token0 * token0_price
                #     total_of_token1 = balance_of_token1 * token1_price
                #     # rate= balance_of_token0/balance_of_token1
                #
                #     total_price= total_of_token0+total_of_token1
                # stake_amount0=
                # elif token0_price == 0:
                #     total_of_token1 = balance_of_token0 * token1_price
                #     total_of_token0 = total_of_token1
                #     token0_price = total_of_token0 / balance_of_token0
                # else:
                #     total_of_token0 = balance_of_token1 * token0_price
                #     total_of_token1 = total_of_token0
                #     token1_price = total_of_token1 / new_amount1
                # lp_token_price = total_price/ total_liquidity
                # result[lp_token].update({
                #     "price": lp_token_price,
                #     # "stakeAmountToken0": lp_token_stake_amount * lp_token_price / 2 / token0_price,
                #     # "stakeAmountToken1": lp_token_stake_amount * lp_token_price / 2 / token1_price
                # })

        return lp_token_info

    ### USER
    def get_all_nft_token_of_user_function(
            self, user: str, block_number: int = "latest"):
        rpc_calls = {}
        web3 = self.state_service.get_w3()
        user = self.checksum_address(web3, user)
        self.nft_token_manager = self.checksum_address(web3, self.nft_token_manager)
        nft_contract = web3.eth.contract(abi=PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI, address=self.nft_token_manager)
        number_token = nft_contract.functions.balanceOf(user).call()
        self.masterchef_addr = self.checksum_address(web3, self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        number_stake_nft_token = master_chef_contract.functions.balanceOf(user).call()

        for idx in range(number_token):
            query_id = f'tokenOfOwnerByIndex_{user}_{idx}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager, abi=self.NFT_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        for idx in range(number_stake_nft_token):
            query_id = f'stakeTokenOfOwnerByIndex_{user}_{idx}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        return rpc_calls

    def decode_all_nft_token_of_user_function(
            self, user_data: dict):
        result = {'allToken': {}, 'stakeToken': {}}
        for query_id, token_id in user_data.items():
            fn_name = query_id.split("_")[0]
            ind = query_id.split("_")[2]
            if fn_name == "tokenofownerbyindex":
                result['allToken'].update(
                    {token_id: {"index": ind}}
                )
            if fn_name == 'staketokenofownerbyindex':
                result['stakeToken'].update({token_id: {"index": ind}})

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = True, block_number: int = "latest"):
        rpc_calls = {}
        user_data= supplied_data['user_data']
        for token_id, value in user_data['allToken'].items():
            query_id = f'positions_{user}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager, abi=self.NFT_abi, fn_name="positions",
                fn_paras=[int(token_id)], block_number=block_number)

        for token_id, value in user_data['stakeToken'].items():
            for fn_name in ['pendingCake', "userPositionInfos"]:
                query_id = f'stake{fn_name}_{user}_{token_id}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=self.masterchef_addr, abi=self.masterchef_abi, fn_name=fn_name,
                    fn_paras=[int(token_id)], block_number=block_number)
        return rpc_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict= None, token_price: dict = None,
                                  stake: bool = True,
                                  block_number: int = "latest"):
        user_data= supplied_data['user_data']
        for token_id, value in user_data['allToken'].items():
            query_id = f'positions_{user}_{token_id}_{block_number}'.lower()
            response = decoded_data.get(query_id)
            liquidity = response[7]
            if liquidity != 0:
                print(f'{token_id}: {liquidity}')
            user_data['allToken'][token_id].update(
                {
                    "liquidity": liquidity,
                    "token0": response[2],
                    "token1": response[3]
                }
            )
        for token_id, value in user_data['stakeToken'].items():
            query_id = f'stakeuserPositionInfos_{user}_{token_id}_{block_number}'.lower()
            user_position_infos = decoded_data.get(query_id)
            pending_cake = decoded_data.get(f'stakependingCake_{user}_{token_id}_{block_number}'.lower())
            liquidity = user_position_infos[0]
            reward = user_position_infos[5]
            pid = user_position_infos[7]
            boost_multiplier = user_position_infos[8]
            user_data['stakeToken'][token_id].update(
                {
                    'pid': pid,
                    "liquidity": liquidity / 10 ** 18,
                    'reward': reward,
                    'boostMultiplier': boost_multiplier,
                    "pendingCake": pending_cake / 10 ** 18
                }
            )

        return user_data

    def convert_q64_96_to_integer(self, sqrt_price_x96):
        integer_part = sqrt_price_x96 >> 96
        fractional_part = (sqrt_price_x96 & ((1 << 96) - 1)) / (2 ** 96)
        # Tổng hợp thành số nguyên
        result = integer_part + fractional_part

        return result

    def checksum_address(self, web3, address):
        if web3.isAddress(address):
            address = web3.toChecksumAddress(address)
        return address
