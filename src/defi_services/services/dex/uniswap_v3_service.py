import logging

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
                    query_id = f'allPool_{token0}_{token1}_{fee}_latest'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        self.factory_addr, self.factory_abi, fn_name="getPool", fn_paras=[token0, token1, fee]
                    )
        return rpc_calls

    def decode_all_supported_lp_token(self, decoded_data, supplied_data: dict = None):
        result = {}
        for query_id, value in decoded_data.items():
            if value != '0x0000000000000000000000000000000000000000':
                token0 = query_id.split("_")[1]
                token1 = query_id.split("_")[2]
                fee = query_id.split("_")[3]

                result[value] = {
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
                query_id = f"{fn_name}_{lp_token}_{block_number}_{self.chain_id}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=UNISWAP_V3_POOL_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        result = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            token0 = value.get("token0")
            token1 = value.get("token1")
            fee = value.get('fee')
            total_liquidity = response_data.get(f'liquidity_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                                0)
            sqrt_price_x96 = response_data.get(f"slot0_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            price = self.convert_q64_96_to_integer(sqrt_price_x96)
            result[lp_token] = {
                "token0": token0,
                'token1': token1,
                'fee': fee,
                "totalLiquidity": total_liquidity / 10 ** 18,
                "currentPrice": price,
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
            self, supplied_data, decoded_data, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        result = {}
        for lp_token, value in lp_token_info.items():
            result[lp_token] = {}
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    balance_of = decoded_data.get(
                        f'balanceOf_{lp_token}_{token}_{block_number}_{self.chain_id}'.lower())
                    decimals = decoded_data.get(f'decimals_{lp_token}_{token}_{block_number}_{self.chain_id}'.lower())
                    result[lp_token].update({
                        f'{fn_name}_amount': balance_of / 10 ** decimals,
                        f'{fn_name}_decimals': decimals
                    })
        return result

    def calculate_lp_token_price_info(
            self, lp_token_info, lp_token_balance):
        for lp_token, value in lp_token_info.items():
            token0 = value.get("token0", None)
            token1 = value.get("token1", None)
            if token0 and token1:
                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                lp_token_info[lp_token].update({
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1
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
            query_id = f'tokenOfOwnerByIndex_{user}_{idx}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        return rpc_calls

    def decode_all_nft_token_of_user_function(
            self, decode_data: dict):
        result = {}

        self.nft_token_manager_addr = self.checksum_address(self.nft_token_manager_addr)
        nft_manager_contract = self.web3.eth.contract(abi=self.nft_token_manager_abi,
                                                      address=self.nft_token_manager_addr)
        for query_id, token_id in decode_data.items():
            fn_name = query_id.split("_")[0]
            if fn_name == "tokenOfOwnerByIndex".lower():
                position = nft_manager_contract.functions.positions(token_id).call()
                fee = position[4]
                token0 = position[2]
                token1 = position[3]

                result.update(
                    {token_id: {"position_id": token_id,
                                'pool_fee': fee,
                                'liquidity': position[7],
                                'tick_lower': position[5],
                                'tick_upper': position[6],
                                'token0_address': token0,
                                'token1_address': token1}}
                )

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = True, block_number: int = "latest"):
        rpc_calls = {}
        user_data = supplied_data['user_data']
        for token_id, value in user_data.items():
            fee = value['pool_fee']
            token0 = self.checksum_address(value['token0_address'])
            token1 = value['token1_address']
            query_id = f'getPool_{user}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.factory_addr, abi=self.factory_abi, fn_name="getPool",
                fn_paras=[token0, token1, int(fee)], block_number=block_number)
            for token in [token0, token1]:
                query_id = f'decimals_{token}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(address=token, abi=ERC20_ABI,
                                                                           fn_name="decimals",
                                                                           block_number=block_number)

        return rpc_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict = None,
                                  stake: bool = True,
                                  block_number: int = "latest"):

        user_data = supplied_data['user_data']
        for token_id, value in user_data.items():
            liquidity = user_data.get(token_id)['liquidity']
            tick_upper = user_data.get(token_id).get('tick_upper')
            tick_lower = user_data.get(token_id).get('tick_lower')
            token0 = user_data.get(token_id).get('token0_address')
            token1 = user_data.get(token_id).get('token1_address')
            pool_addr = decoded_data.get(f'getPool_{user}_{token_id}_{block_number}'.lower())
            token0_decimals = decoded_data.get(f'decimals_{token0}_{block_number}'.lower())
            token1_decimals = decoded_data.get(f'decimals_{token1}_{block_number}'.lower())

            if liquidity != 0:
                pool_contract = self.web3.eth.contract(abi=self.pool_info['pool_abi'],
                                                       address=self.checksum_address(pool_addr))
                slot0 = pool_contract.functions.slot0().call()
                sqrt_price_x96 = slot0[0]
                tick = slot0[1]
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
            # except Exception as e:
            #     logger.error(f"[Ignored] An exception when decode data from provider: {e}")
            #     continue

        return user_data

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
        # Tổng hợp thành số nguyên
        result = integer_part + fractional_part

        return result


class FixedPoint96:
    RESOLUTION = 96
    Q96 = 0x1000000000000000000000000
