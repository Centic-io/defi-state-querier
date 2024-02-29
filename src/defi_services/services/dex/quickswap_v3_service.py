import logging
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.quickswap_info import QUICKSWAP_POLYGON_V3_INFO
from defi_services.services.dex.uniswap_v3_service import UniswapV3Services
from defi_services.utils.get_fees import get_fees

logger = logging.getLogger("QuickSwap V3 State Service")


class QuickSwapV3Info:
    mapping = {
        Chain.polygon: QUICKSWAP_POLYGON_V3_INFO
    }


class QuickSwapV3Services(UniswapV3Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__(state_service, chain_id)
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = QuickSwapV3Info.mapping.get(chain_id)
        self.web3 = self.state_service.get_w3()
        if self.pool_info is not None:
            self.factory_abi = self.pool_info.get('factory_abi')
            self.nft_token_manager_addr = self.pool_info.get('NFT_manager_address')
            self.nft_token_manager_abi = self.pool_info.get('NFT_manager_abi')
            self.factory_addr = self.pool_info.get('factory_address')

    def get_service_info(self):
        info = {
            Dex.quickswap_v3: {
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
                query_id = f'allPool_{self.factory_addr}_{[token0, token1]}_latest'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    self.factory_addr, self.factory_abi, fn_name="poolByPair", fn_paras=[token0, token1]
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
                query_id = f'allPool_{self.factory_addr}_{[token0, token1]}_latest'.lower()
                pool_address = decoded_data.get(query_id)
                if pool_address != '0x0000000000000000000000000000000000000000':
                    result[pool_address] = {
                        'token0': token0,
                        'token1': token1,
                    }

        return result

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for fn_name in ["liquidity", "globalState", 'tickSpacing']:
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
            slot0 = response_data.get(f"globalState_{lp_token}_{block_number}".lower())
            price = (slot0[0] / 2 ** 96) ** 2
            token0_address = value.get('token0')
            token1_address = value.get('token1')
            token0_decimals = response_data.get(f'decimals_{token0_address}_{block_number}'.lower())
            token1_decimals = response_data.get(f'decimals_{token1_address}_{block_number}'.lower())
            tick_spacing = response_data.get(f'tickSpacing_{lp_token}_{block_number}'.lower())

            lp_token_info[lp_token].update({
                "liquidity_in_range": liquidity_in_range,
                "price": price,
                'tick': slot0[1],
                'fee': slot0[2],
                'tick_spacing': tick_spacing,
                'token0_decimals': token0_decimals,
                'token1_decimals': token1_decimals

            })
        return lp_token_info

    ###USER
    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict = None, stake: bool = False,
                                  block_number: int = "latest"):
        user_data = supplied_data['user_data']
        user_data_with_liquidity = {}
        for token_id, value in user_data.items():
            position = decoded_data.get(f'positions_{self.nft_token_manager_addr}_{token_id}_{block_number}'.lower())
            liquidity = position[6]
            if liquidity > 0:
                user_data_with_liquidity[token_id] = {
                    'token0': position[2],
                    'token1': position[3],
                    'tick_lower': position[4],
                    'tick_upper': position[5],
                    'liquidity': liquidity,
                    'fee_growth_inside0_x128': position[7],
                    'fee_growth_inside1_x128': position[8],
                }
        return user_data_with_liquidity

    def get_user_token_amount_function(self, user: str, supplied_data: dict, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        rpc_calls = {}
        for token_id, value in user_data.items():
            token0 = value.get('token0')
            token1 = value.get('token1')
            query_id = f'getPool_{self.factory_addr}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                self.factory_addr, self.factory_abi, fn_name="poolByPair", fn_paras=[token0, token1]
            )
            for token_key in ['token0', 'token1']:
                token_address = value.get(token_key)

                query_id = f'decimals_{token_address}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=token_address, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def get_rewards_balance_function_info(self, user, supplied_data, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        rpc_calls = {}
        for token_id, value in user_data.items():
            lp_token_address = value.get('pool_address')
            tick_lower = value.get('tick_lower')
            tick_upper = value.get('tick_upper')
            for fnc in ['totalFeeGrowth0Token', 'totalFeeGrowth1Token']:
                query_id = f'{fnc}_{lp_token_address}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token_address, abi=self.pool_info['pool_abi'], fn_name=fnc)

            for param in [tick_lower, tick_upper]:
                query_id = f'ticks_{lp_token_address}_{param}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token_address, abi=self.pool_info['pool_abi'], fn_name="ticks", fn_paras=[param])

        return rpc_calls

    def calculate_rewards_balance(
            self, user: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        user_data = supplied_data['user_data']

        for token_id, value in user_data.items():
            lp_token_address = value.get('pool_address')
            tick_lower = value.get('tick_lower')
            tick_upper = value.get('tick_upper')
            fee_growth_inside_0_x128 = value.get('fee_growth_inside0_x128')
            fee_growth_inside_1_x128 = value.get('fee_growth_inside1_x128')
            fee_growth_global_0 = decoded_data.get(
                f'totalFeeGrowth0Token_{lp_token_address}_{block_number}'.lower())
            fee_growth_global_1 = decoded_data.get(
                f'totalFeeGrowth1Token_{lp_token_address}_{block_number}'.lower())
            fee_growth_0_low_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_lower}_{block_number}'.lower())[2]
            fee_growth_1_low_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_lower}_{block_number}'.lower())[3]
            fee_growth_0_hi_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_upper}_{block_number}'.lower())[2]
            fee_growth_1_hi_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_upper}_{block_number}'.lower())[3]
            liquidity = value.get('liquidity')
            tick = lp_token_info.get(lp_token_address, {}).get('tick')
            token0_decimals = lp_token_info.get(lp_token_address, {}).get("token0_decimals")
            token1_decimals = lp_token_info.get(lp_token_address, {}).get("token1_decimals")
            if tick and token0_decimals and token1_decimals:
                token0_reward, token1_reward = get_fees(
                    fee_growth_global_0=fee_growth_global_0,
                    fee_growth_global_1=fee_growth_global_1,
                    fee_growth_0_low=fee_growth_0_low_x128,
                    fee_growth_1_low=fee_growth_1_low_x128,
                    fee_growth_0_hi=fee_growth_0_hi_x128,
                    fee_growth_1_hi=fee_growth_1_hi_x128,
                    fee_growth_inside_0=fee_growth_inside_0_x128,
                    fee_growth_inside_1=fee_growth_inside_1_x128,
                    liquidity=liquidity, tick_lower=tick_lower,
                    tick_upper=tick_upper, tick_current=tick,
                    decimals0=token0_decimals, decimals1=token1_decimals)

                user_data[token_id].update({
                    'token0_reward': token0_reward,
                    'token1_reward': token1_reward
                })

        return user_data