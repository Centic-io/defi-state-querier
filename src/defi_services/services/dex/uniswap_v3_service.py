import copy
import logging
import math

from web3 import Web3

from defi_services.abis.dex.uniswap.pool_v3_abi import UNISWAP_V3_POOL_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.uniswap_info import UNISWAP_V3_ETH_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices

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
                "pool_info": self.pool_info
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
            for fn_name in ["liquidity", "slot0"]:
                query_id = f"{fn_name}_{lp_token}_{self.factory_addr}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=UNISWAP_V3_POOL_ABI, fn_name=fn_name, fn_paras=None,
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
            total_liquidity = response_data.get(f'liquidity_{lp_token}_{self.factory_addr}_{block_number}'.lower(), 0)
            slot0 = response_data.get(f"slot0_{lp_token}_{self.factory_addr}_{block_number}".lower())
            price = self.convert_q64_96_to_integer(slot0[0]) ** 2
            token0_address = value.get('token0')
            token1_address = value.get('token1')
            token0_decimals = response_data.get(f'decimals_{token0_address}_{block_number}'.lower())
            token1_decimals = response_data.get(f'decimals_{token1_address}_{block_number}'.lower())

            lp_token_info[lp_token].update({
                "totalLiquidity": total_liquidity,
                "price": price,
                'tick': slot0[1],
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
                    lp_token_info[lp_token][f'{token_key}Amount'] = balance_of / 10 ** decimals

        return lp_token_info

    # def calculate_lp_token_price_info(
    #         self, lp_token_info, lp_token_balance):
    #     for lp_token, value in lp_token_info.items():
    #         token0 = value.get("token0", None)
    #         token1 = value.get("token1", None)
    #         if token0 and token1:
    #             balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
    #             balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
    #             lp_token_info[lp_token].update({
    #                 "token0Amount": balance_of_token0,
    #                 "token1Amount": balance_of_token1
    #             })
    #     return lp_token_info

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

        for token_id, value in user_data.items():
            lp_token_address = decoded_data.get(f'allPool_{self.factory_addr}_{token_id}_{block_number}'.lower())
            user_data[token_id].update({
                'poolAddress': lp_token_address
            })
            liquidity = value.get('liquidity')
            if liquidity > 0:
                token0 = value.get('token0')
                token1 = value.get('token1')
                token0_decimals = decoded_data.get(f'decimals_{token0}_{block_number}'.lower())
                token1_decimals = decoded_data.get(f'decimals_{token1}_{block_number}'.lower())
                price = lp_token_info.get(lp_token_address, {}).get("price")

                tick = lp_token_info.get(lp_token_address, {}).get('tick')
                tick_upper = value.get('tickUpper')
                tick_lower = value.get('tickLower')
                if price and tick:
                    sqrt_price_x96 = self.convert_integer_to_q64_96(math.sqrt(price))

                    token0_amount, token1_amount = self.get_amount0_amount1(liquidity=liquidity,
                                                                            sqrt_price_x96=sqrt_price_x96,
                                                                            tick=tick, tick_upper=tick_upper,
                                                                            tick_lower=tick_lower)
                    user_data[token_id].update(
                        {

                            'token0_amount': token0_amount / 10 ** token0_decimals,
                            'token1_amount': token1_amount / 10 ** token1_decimals,

                        }
                    )

        return user_data

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

    def get_amount0_amount1(self, liquidity, sqrt_price_x96, tick, tick_lower, tick_upper):
        def _get_sqrt_ratio_at_tick(tick):
            MAX_TICK = 887272
            abs_tick = abs(tick)
            if abs_tick > MAX_TICK:
                raise ValueError('T')

            ratio = 0xfffcb933bd6fad37aa2d162d1a594001 if abs_tick & 0x1 else 0x100000000000000000000000000000000
            ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128 if abs_tick & 0x2 else ratio
            ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128 if abs_tick & 0x4 else ratio
            ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128 if abs_tick & 0x8 else ratio
            ratio = (ratio * 0xffcb9843d60f6159c9db58835c926644) >> 128 if abs_tick & 0x10 else ratio
            ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128 if abs_tick & 0x20 else ratio
            ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128 if abs_tick & 0x40 else ratio
            ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128 if abs_tick & 0x80 else ratio
            ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128 if abs_tick & 0x100 else ratio
            ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128 if abs_tick & 0x200 else ratio
            ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128 if abs_tick & 0x400 else ratio
            ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128 if abs_tick & 0x800 else ratio
            ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128 if abs_tick & 0x1000 else ratio
            ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128 if abs_tick & 0x2000 else ratio
            ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128 if abs_tick & 0x4000 else ratio
            ratio = (ratio * 0x31be135f97d08fd981231505542fcfa6) >> 128 if abs_tick & 0x8000 else ratio
            ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128 if abs_tick & 0x10000 else ratio
            ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128 if abs_tick & 0x20000 else ratio
            ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128 if abs_tick & 0x40000 else ratio
            ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128 if abs_tick & 0x80000 else ratio

            if tick > 0:
                ratio = (2 ** 256 - 1) // ratio

            sqrt_price_x96 = (ratio >> 32) + (0 if ratio % (1 << 32) == 0 else 1)
            return sqrt_price_x96

        #
        def _get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, round_up):
            if sqrt_ratio_ax96 > sqrt_ratio_bx96:
                sqrt_ratio_ax96, sqrt_ratio_bx96 = sqrt_ratio_bx96, sqrt_ratio_ax96
            numerator1 = liquidity << FixedPoint96.RESOLUTION
            numerator2 = sqrt_ratio_bx96 - sqrt_ratio_ax96
            if sqrt_ratio_ax96 < 0:
                return None
            else:
                if round_up:
                    x = _mul_div_rounding_up(numerator1, numerator2, sqrt_ratio_bx96)
                    return _div_rounding_up(x, sqrt_ratio_ax96)
                else:
                    return (numerator1 * numerator2 / sqrt_ratio_bx96) / sqrt_ratio_ax96

        def _get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, round_up):
            if sqrt_ratio_ax96 > sqrt_ratio_bx96:
                sqrt_ratio_ax96, sqrt_ratio_bx96 = sqrt_ratio_bx96, sqrt_ratio_ax96
            if round_up:
                x = _mul_div_rounding_up(liquidity, sqrt_ratio_bx96 - sqrt_ratio_ax96, FixedPoint96.Q96)
                return x
            else:
                return liquidity * (sqrt_ratio_bx96 - sqrt_ratio_ax96) / FixedPoint96.Q96

        def _get_amount0_delta(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity):
            if liquidity < 0:
                return -_get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, -liquidity, False)
            else:
                return _get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, True)

        def _get_amount1_delta(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity):
            if liquidity < 0:
                return -_get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, -liquidity, False)
            else:
                return _get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, True)

        def _div_rounding_up(x, y):
            return x // y + (x % y > 0)

        def _mul_div_rounding_up(a, b, denominator):
            result = a * b / denominator
            if (a * b) % denominator > 0:
                if result < 2 ** 256 - 1:
                    result += 1
                else:
                    raise OverflowError("Result exceeds maximum uint256 value.")
            return result

        amount0, amount1 = 0, 0
        if liquidity != 0:
            if tick < tick_lower:
                amount0 = _get_amount0_delta(_get_sqrt_ratio_at_tick(tick_lower), _get_sqrt_ratio_at_tick(tick_upper),
                                             liquidity)
            elif tick < tick_upper:
                amount0 = _get_amount0_delta(sqrt_price_x96, _get_sqrt_ratio_at_tick(tick_upper), liquidity)
                amount1 = _get_amount1_delta(_get_sqrt_ratio_at_tick(tick_lower), sqrt_price_x96, liquidity)
            else:
                amount1 = _get_amount1_delta(_get_sqrt_ratio_at_tick(tick_lower), _get_sqrt_ratio_at_tick(tick_upper),
                                             liquidity)
        return amount0, amount1

    def checksum_address(self, address):
        if self.web3.isAddress(address):
            address = self.web3.toChecksumAddress(address)
        return address

    def convert_q64_96_to_integer(self, sqrt_price_x96):
        integer_part = sqrt_price_x96 >> 96
        fractional_part = (sqrt_price_x96 & ((1 << 96) - 1)) / (2 ** 96)
        result = integer_part + fractional_part

        return result

    def convert_integer_to_q64_96(self, integer):
        integer_part = int(integer)
        fractional_part = int((integer - integer_part) * (2 ** 96))
        result = (integer_part << 96) + fractional_part
        return result


class FixedPoint96:
    RESOLUTION = 96
    Q96 = 0x1000000000000000000000000
