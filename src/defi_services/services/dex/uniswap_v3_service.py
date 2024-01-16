import copy
import logging
import math
from web3 import Web3
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.uniswap_info import UNISWAP_V3_ETH_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices
from defi_services.utils.sqrt_price_math import get_token_amount_of_user

logger = logging.getLogger("UniSwap V3 State Service")


class UniswapV3Info:
    mapping = {
        Chain.ethereum: UNISWAP_V3_ETH_INFO
    }


class UniswapV3Services(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = UniswapV3Info.mapping.get(chain_id)
        self.web3 = self.state_service.get_w3()
        if self.pool_info is not None:
            self.factory_abi = self.pool_info.get('factory_abi')
            self.nft_token_manager_addr = self.pool_info.get('NFT_manager_address')
            self.nft_token_manager_abi = self.pool_info.get('NFT_manager_abi')
            self.factory_addr = self.pool_info.get('factory_address')

    def get_service_info(self):
        info = {
            Dex.uniswap_v3: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit: int = 100, supplied_data: dict = None):
        rpc_calls = {}
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)
        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 3000, 10000]:
                    query_id = f'allPool_{self.factory_addr}_{[token0, token1, fee]}_latest'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        self.factory_addr, self.factory_abi, fn_name="getPool", fn_paras=[token0, token1, fee]
                    )
        return rpc_calls

    def decode_all_supported_lp_token(self, limit: int = 100, decoded_data: dict = None, supplied_data: dict = None):
        result = {}
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)
        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 3000, 10000]:
                    query_id = f'allPool_{self.factory_addr}_{[token0, token1, fee]}_latest'.lower()
                    pool_address = decoded_data.get(query_id)
                    if pool_address != '0x0000000000000000000000000000000000000000':
                        result[pool_address] = {
                            'token0': token0,
                            'token1': token1,
                            'fee': fee
                        }

        return result

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for fn_name in ["liquidity", "slot0", 'tickSpacing']:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=self.pool_info['pool_abi'], fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

            for token_key in ['token0', 'token1']:
                token_address = value.get(token_key)
                query_id = f'decimals_{token_address}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=token_address, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            liquidity_in_range = response_data.get(f'liquidity_{lp_token}_{block_number}'.lower(), 0)
            slot0 = response_data.get(f"slot0_{lp_token}_{block_number}".lower())
            price = (slot0[0] / 2 ** 96) ** 2
            token0_address = value.get('token0')
            token1_address = value.get('token1')
            token0_decimals = response_data.get(f'decimals_{token0_address}_{block_number}'.lower())
            token1_decimals = response_data.get(f'decimals_{token1_address}_{block_number}'.lower())
            tick_spacing = response_data.get(f'tickSpacing_{lp_token}_{block_number}'.lower())

            lp_token_info[lp_token].update({
                "liquidityInRange": liquidity_in_range,
                "price": price,
                'tick': slot0[1],
                'tickSpacing': tick_spacing,
                'token0Decimals': token0_decimals,
                'token1Decimals': token1_decimals

            })
        return lp_token_info

    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for token_key in ["token0", "token1"]:
                token_address = value.get(token_key, None)
                if token_address is not None:
                    balance_query_id = f'balanceOf_{token_address}_{lp_token}_{block_number}'.lower()
                    decimals_query_id = f'decimals_{token_address}_{block_number}'.lower()

                    rpc_calls[balance_query_id] = self.state_service.get_function_info(
                        address=token_address, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[lp_token],
                        block_number=block_number)

                    rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                        address=token_address, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(
            self, supplied_data, decoded_data, block_number: int = "latest"):
        lp_token_info = {}
        for lp_token, value in supplied_data['lp_token_info'].items():
            lp_token_info[lp_token] = copy.deepcopy(value)
            for token_key in ["token0", "token1"]:
                token_address = value.get(token_key, None)
                decimals = decoded_data.get(f'decimals_{token_address}_{block_number}'.lower())

                if token_address is not None:
                    balance_of = decoded_data.get(
                        f'balanceOf_{token_address}_{lp_token}_{block_number}'.lower())
                    lp_token_info[lp_token][f'{token_key}TotalAmount'] = balance_of / 10 ** decimals

            tick = value.get('tick')
            tick_spacing = value.get('tickSpacing')
            tick_lower = tick // tick_spacing * tick_spacing
            tick_upper = (tick // tick_spacing + 1) * tick_spacing
            liquidity = value.get('liquidityInRange')
            sqrt_price_x96 = math.sqrt(value.get('price')) * 2 ** 96
            amount0, amount1 = get_token_amount_of_user(liquidity=liquidity, sqrt_price_x96=sqrt_price_x96, tick=tick,
                                                        tick_lower=tick_lower, tick_upper=tick_upper)
            lp_token_info[lp_token].update({
                'token0AmountInRange': amount0 / 10 ** value.get('token0Decimals'),
                'token1AmountInRange': amount1 / 10 ** value.get('token1Decimals')
            })

        return lp_token_info

    ### USER
    def get_all_nft_token_of_user_function(
            self, user: str, block_number: int = "latest"):
        rpc_calls = {}
        user = self.checksum_address(user)
        self.nft_token_manager_addr = self.checksum_address(self.nft_token_manager_addr)
        nft_contract = self.web3.eth.contract(abi=self.nft_token_manager_abi,
                                              address=self.nft_token_manager_addr)
        number_token = nft_contract.functions.balanceOf(user).call()
        for idx in range(number_token):
            query_id = f'tokenOfOwnerByIndex_{self.nft_token_manager_addr}_{[user, idx]}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        return rpc_calls

    def decode_all_nft_token_of_user_function(
            self, decode_data: dict):
        result = {}
        for query_id, token_id in decode_data.items():
            contract_addr = query_id.split("_")[1]
            if contract_addr == self.nft_token_manager_addr.lower():
                result[token_id] = {}

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = False, block_number: int = "latest"):
        rpc_calls = {}
        user_data = supplied_data['user_data']
        for token_id, _ in user_data.items():
            query_id = f'positions_{self.nft_token_manager_addr}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="positions",
                fn_paras=[int(token_id)], block_number=block_number)
        return rpc_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict = None, stake: bool = False,
                                  block_number: int = "latest"):
        user_data = supplied_data['user_data']
        for token_id, value in user_data.items():
            position = decoded_data.get(f'positions_{self.nft_token_manager_addr}_{token_id}_{block_number}'.lower())
            user_data[token_id].update({
                'token0': position[2],
                'token1': position[3],
                'fee': position[4],
                'tickLower': position[5],
                'tickUpper': position[6],
                'liquidity': position[7],
                'feeGrowthInside0': position[8],
                'feeGrowthInside1': position[9],
                'tokensOwed0': position[10],
                'tokensOwed1': position[11]

            })
        return user_data

    def get_user_token_amount_function(self, user: str, supplied_data: dict, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        rpc_calls = {}
        for token_id, value in user_data.items():
            token0 = value.get('token0')
            token1 = value.get('token1')
            fee = value.get('fee')
            query_id = f'allPool_{self.factory_addr}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                self.factory_addr, self.factory_abi, fn_name="getPool", fn_paras=[token0, token1, fee]
            )
            for token_key in ['token0', 'token1']:
                token_address = value.get(token_key)

                query_id = f'decimals_{token_address}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=token_address, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_user_token_amount_function(self, user: str, supplied_data: dict, decoded_data: dict = None,
                                          block_number: int = "latest"):
        user_data = supplied_data['user_data']
        lp_token_info = supplied_data['lp_token_info']
        result = {}

        for token_id, value in user_data.items():
            lp_token_address = decoded_data.get(f'allPool_{self.factory_addr}_{token_id}_{block_number}'.lower())
            user_data[token_id].update({
                'poolAddress': lp_token_address
            })
            liquidity = value.get('liquidity')
            if liquidity > 0:
                result[token_id] = copy.deepcopy(user_data[token_id])
                token0 = value.get('token0')
                token1 = value.get('token1')
                token0_decimals = decoded_data.get(f'decimals_{token0}_{block_number}'.lower())
                token1_decimals = decoded_data.get(f'decimals_{token1}_{block_number}'.lower())
                price = lp_token_info.get(lp_token_address, {}).get("price")

                tick = lp_token_info.get(lp_token_address, {}).get('tick')
                tick_upper = value.get('tickUpper')
                tick_lower = value.get('tickLower')
                if price and tick:
                    sqrt_price_x96 = (math.sqrt(price)) * 2 ** 96

                    token0_amount, token1_amount = get_token_amount_of_user(liquidity=liquidity,
                                                                            sqrt_price_x96=sqrt_price_x96,
                                                                            tick=tick, tick_upper=tick_upper,
                                                                            tick_lower=tick_lower)
                    result[token_id].update(
                        {
                            'token0_amount': token0_amount / 10 ** token0_decimals,
                            'token1_amount': token1_amount / 10 ** token1_decimals,

                        }
                    )

        return result

    def get_rewards_balance_function_info(self, user, supplied_data, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        rpc_calls = {}
        for token_id, value in user_data.items():
            lp_token_address = value.get('poolAddress')
            tick_lower = value.get('tickLower')
            tick_upper = value.get('tickUpper')
            position_key = self.get_position_key(tick_lower, tick_upper)
            query_id = f'positions_{lp_token_address}_{[tick_upper, tick_lower]}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token_address, abi=self.pool_info['pool_abi'], fn_name="positions", fn_paras=[position_key]
            )
        return rpc_calls

    def calculate_rewards_balance(
            self, user: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        user_data = supplied_data['user_data']

        for token_id, value in user_data.items():
            liquidity = value.get('liquidity')
            if liquidity > 0:
                lp_token_address = value.get('poolAddress')
                tick_lower = value.get('tickLower')
                tick_upper = value.get('tickUpper')
                pool_position = decoded_data.get(
                    f'positions_{lp_token_address}_{[tick_upper, tick_lower]}_{block_number}'.lower())

                pool_fee_growth_inside0 = pool_position[1]
                pool_fee_growth_inside1 = pool_position[2]
                fee_growth_inside0 = value.get('feeGrowthInside0')
                fee_growth_inside1 = value.get('feeGrowthInside1')
                liquidity = value.get('liquidity')
                token0_decimals = lp_token_info.get(lp_token_address, {}).get("token0Decimals")
                token1_decimals = lp_token_info.get(lp_token_address, {}).get("token1Decimals")
                token0_reward = ((pool_fee_growth_inside0 - fee_growth_inside0) / 2 ** 128 * liquidity + value.get(
                    'tokensOwed0')) / 10 ** token0_decimals
                token1_reward = ((pool_fee_growth_inside1 - fee_growth_inside1) / 2 ** 128 * liquidity + value.get(
                    'tokensOwed1')) / 10 ** token1_decimals
                if token0_reward > 0 or token1_reward > 0:
                    print(token_id)

            else:
                token0_reward = 0
                token1_reward = 0

            user_data[token_id].update({
                'token0Reward': token0_reward,
                'token1Reward': token1_reward
            })

        return user_data

    def get_position_key(self, tick_lower, tick_upper):
        data_to_hash = Web3.solidityKeccak(
            ['address', 'int24', 'int24'],
            [Web3.toChecksumAddress(self.nft_token_manager_addr), tick_lower, tick_upper]
        )
        return data_to_hash.hex()

    def checksum_address(self, address):
        if self.web3.isAddress(address):
            address = self.web3.toChecksumAddress(address)
        return address
