import logging

from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.v3_pool_abi import PANCAKESWAP_V3_POOL_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.pancakeswap_info import PANCAKESWAP_V3_BSC_INFO
from defi_services.services.dex.uniswap_v3_service import UniswapV3Services
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("PancakeSwap V3 State Service")


class PancakeSwapV3Info:
    mapping = {
        Chain.bsc: PANCAKESWAP_V3_BSC_INFO
    }


class PancakeSwapV3Service(UniswapV3Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__(state_service=state_service, chain_id=chain_id)
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = PancakeSwapV3Info.mapping.get(chain_id)
        self.web3 = self.state_service.get_w3()

        if self.pool_info is not None:
            self.masterchef_addr = self.pool_info['master_chef_address']
            self.masterchef_abi = self.pool_info['master_chef_abi']
            self.factory_addr = self.pool_info['factory_address']
            self.factory_abi = self.pool_info.get('factory_abi')
            self.nft_token_manager_addr = self.pool_info['NFT_manager_address']
            self.nft_token_manager_abi = self.pool_info['NFT_manager_abi']

    def get_service_info(self):
        info = {
            Dex.pancake_v3: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_farming_supported_lp_token(self, limit: int = 1, supplied_data: dict = None):
        web3 = self.state_service.get_w3()
        self.masterchef_addr = self.checksum_address(self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.poolLength().call()
        rpc_calls = {}
        for pid in range(1, min(pool_length, limit)):
            query_id = f'poolInfo_{pid}_'
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[pid]
            )

        return rpc_calls

    def decode_farming_supported_lp_token(self, response_data, supplied_data: dict = None):
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
                # 'stakeBoostLiquidity': value[6]
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
            # query_id = f'getLatestPeriodInfoByPid_{lp_token}_{block_number}_{self.chain_id}'.lower()
            # rpc_calls[query_id] = self.state_service.get_function_info(
            #     address=self.masterchef_addr, abi=self.masterchef_abi, fn_name='getLatestPeriodInfoByPid',
            #     fn_paras=[int(pid)],
            #     block_number=block_number)
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
            # stake_boost_liquidity = value.get('stakeBoostLiquidity')
            unstake_liquidity = response_data.get(f'liquidity_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                                  0)
            sqrt_price_x96 = response_data.get(f"slot0_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            price = self.convert_q64_96_to_integer(sqrt_price_x96)
            # cake_per_second = response_data.get(f"getLatestPeriodInfoByPid_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            result[lp_token] = {
                "pid": pid,
                "token0": token0,
                'token1': token1,
                'fee': fee,
                'stakeLiquidity': stake_liquidity,
                # 'stakeBoostLiquidity': stake_boost_liquidity / 10 ** 18,
                "unstakeLiquidity": unstake_liquidity,
                "currentPrice": price,
                # "cakePerSecond": cake_per_second / 10 ** 18
            }
        return result

    ### USER
    def get_all_nft_token_of_user_function(
            self, user: str, block_number: int = "latest"):
        rpc_calls = super().get_all_nft_token_of_user_function(user, block_number)
        user = self.checksum_address(user)
        self.masterchef_addr = self.checksum_address(self.masterchef_addr)
        master_chef_contract = self.web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        number_stake_nft_token = master_chef_contract.functions.balanceOf(user).call()
        for idx in range(number_stake_nft_token):
            query_id = f'stakeTokenOfOwnerByIndex_{user}_{idx}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        return rpc_calls

    def decode_all_nft_token_of_user_function(
            self, decode_data: dict):
        result = {'allToken': {}, 'stakeToken': {}}
        result['allToken'] = super().decode_all_nft_token_of_user_function(decode_data)
        self.masterchef_addr = self.checksum_address(self.masterchef_addr)
        master_chef_contract = self.web3.eth.contract(abi=self.masterchef_abi,
                                                      address=self.masterchef_addr)
        for query_id, token_id in decode_data.items():
            fn_name = query_id.split("_")[0]

            if fn_name == 'stakeTokenOfOwnerByIndex'.lower():
                position = master_chef_contract.functions.userPositionInfos(token_id).call()
                liquidity = position[0]
                tick_lower = position[2]
                tick_upper = position[3]
                reward = position[5]
                pid = position[7]

                result['stakeToken'][token_id] = {
                    'stake_liquidity': liquidity,
                    'tickLower': tick_lower,
                    'tickUpper': tick_upper,
                    'reward': reward,
                    'pid': pid
                }

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = True, block_number: int = "latest"):
        stake_tokens = supplied_data['user_data']['stakeToken']
        supplied_param = {'user_data': supplied_data['user_data']['allToken']}
        rpc_calls = super().get_user_info_function(user, supplied_param, stake, block_number)

        for token_id, value in stake_tokens.items():
            pid = value['pid']
            query_id = f'poolInfo_{user}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[pid]
            )

            query_id = f'pendingCake_{user}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="pendingCake", fn_paras=[int(token_id)]
            )

        return rpc_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict = None,
                                  stake: bool = True,
                                  block_number: int = "latest"):
        user_data = supplied_data['user_data']
        lp_token_info = supplied_data['lp_token_info']
        supplied_param = {'user_data': user_data['allToken']}
        user_data['allToken'] = super().decode_user_info_function(user, supplied_param, decoded_data, stake,
                                                                  block_number)
        for token_id, value in user_data['stakeToken'].items():
            liquidity = value.get('stake_liquidity')
            tick_lower = value.get('tickLower')
            tick_upper = value.get('tickUpper')
            pool_addr = decoded_data.get(f'poolInfo_{user}_{token_id}_{block_number}'.lower())[1]
            pending_cake = decoded_data.get(f'pendingCake_{user}_{token_id}_{block_number}'.lower())
            token0_decimals = lp_token_info.get(pool_addr, {}).get('token0_decimals', 18)
            token1_decimals = lp_token_info.get(pool_addr, {}).get('token1_decimals', 18)
            if liquidity:
                pool_contract = self.web3.eth.contract(abi=self.pool_info['pool_abi'],
                                                       address=self.checksum_address(pool_addr))
                slot0 = pool_contract.functions.slot0().call()
                sqrt_price_x96 = slot0[0]
                tick = slot0[1]
                token0_amount, token1_amount = self.get_amount0_amount1(liquidity=liquidity,
                                                                        sqrt_price_x96=sqrt_price_x96,
                                                                        tick=tick, tick_upper=tick_upper,
                                                                        tick_lower=tick_lower)
                user_data['stakeToken'][token_id].update({
                    'reward': pending_cake / 10 ** 18,
                    'stake_token0_amount': token0_amount / 10 ** token0_decimals,
                    'stake_token1_amount': token1_amount / 10 ** token1_decimals,
                })

        return user_data
