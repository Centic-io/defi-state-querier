import logging

from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.quickswap_info import QUICKSWAP_POLYGON_V2_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("QuickSwap V2 State Service")


class QuickSwapV2Info:
    mapping = {
        Chain.polygon: QUICKSWAP_POLYGON_V2_INFO
    }


class QuickSwapV2Services(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = QuickSwapV2Info.mapping.get(chain_id)
        self.masterchef_addr = self.pool_info['factoryAddress']
        self.masterchef_abi = self.pool_info['factory_abi']

    def get_service_info(self):
        info = {
            Dex.quickswap_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                "pool_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit=1):
        web3 = self.state_service.get_w3()
        if web3.isAddress(self.masterchef_addr):
            self.masterchef_addr = web3.toChecksumAddress(self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.allPairsLength().call()
        rpc_calls = {}

        for pid in range(0, int(pool_length / limit)):
            query_id = f'lpToken_{pid}_'
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="allPairs", fn_paras=[pid]
            )
        return rpc_calls

    def decode_all_supported_lp_token(self, response_data):
        result = {}
        for key, value in response_data.items():
            pid = key.split("_")[1]
            result[value] = {
                "pid": pid}
        return result

    def get_important_lp_token(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_list = supplied_data['lp_token_list']
        for lp_token, value in lp_token_list.items():
            for fn_name in ["token0", "token1"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

        return rpc_calls

    def decode_important_lp_token(self, supplied_data, response_data, block_number: int = "latest"):
        lp_token_list = supplied_data['lp_token_list']
        token_info = supplied_data['token_info']
        result = {}
        for lp_token, value in lp_token_list.items():
            pid = value.get('pid')
            token0 = response_data.get(f'token0_{lp_token}_{block_number}'.lower(), "")
            token1 = response_data.get(f'token1_{lp_token}_{block_number}'.lower(), "")
            # chỉ lấy những token mà có dữ liệu lưu trong database và có gía
            if token0 in token_info and token1 in token_info:
                result[lp_token] = {
                    'pid': pid,
                    "token0": token0,
                    "token1": token1
                }

        return result

    def get_lp_token_function_info(self, lp_token_info, block_number: int = "latest"):
        rpc_calls = {}
        for lp_token, value in lp_token_info.items():
            for fn_name in ["decimals", "totalSupply", "name"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, lp_token_info, response_data, block_number: int = "latest"):
        result = {}
        for lp_token, value in lp_token_info.items():
            pid = value.get('pid')
            token0 = value.get('token0')
            token1 = value.get('token1')
            decimals = response_data.get(f'decimals_{lp_token}_{block_number}'.lower(), "")
            total_supply = response_data.get(f'totalSupply_{lp_token}_{block_number}'.lower(), "") / 10 ** decimals
            name = response_data.get(f'name_{lp_token}_{block_number}'.lower(), "")
            result[lp_token] = {
                "pid": pid,
                "totalSupply": total_supply,
                "token0": token0,
                "token1": token1,
                "name": name,
                'decimals': decimals
            }

        return result

    # Get balance of token
    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{lp_token}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{lp_token}_{token}_{block_number}_{self.chain_id}'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[lp_token],
                        block_number=block_number)

                    rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(
            self, supplied_data, balance_info, block_number: int = "latest"):
        lp_token_balance = {}
        lp_token_info = supplied_data['lp_token_info']
        token_info = supplied_data['token_info']
        for key, value in lp_token_info.items():
            lp_token_balance[key] = {}
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals = balance_info.get(f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower())
                    lp_token_balance[key][token] = balance_info.get(query_id) / 10 ** decimals
        result = self.calculate_lp_token_price_info(lp_token_info, lp_token_balance, token_info)
        return result

    def calculate_lp_token_price_info(
            self, lp_token_info, lp_token_balance, token_info):
        for lp_token, value in lp_token_info.items():
            total_supply = value.get("totalSupply")
            token0 = value.get("token0", 0)
            token1 = value.get("token1", 0)
            if token0 and token1:
                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                token0_price = token_info.get(token0)['price']
                token1_price = token_info.get(token1)['price']
                total_of_token0 = balance_of_token0 * token0_price
                total_of_token1 = balance_of_token1 * token1_price
                lp_token_price = (total_of_token0 + total_of_token1) / total_supply
                lp_token_info[lp_token].update({
                    "totalSupply": total_supply,
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1,
                    'price': lp_token_price
                })
        return lp_token_info

    # ### USER
    def get_user_info_function(
            self, user: str, supplied_data, stake: bool = True, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        # lượng token đang hold trong ví
        for lp_token, value in lp_token_info.items():
            query_id = f'balanceOf_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf",
                fn_paras=[user],
                block_number=block_number)
            decimals_query_id = f'decimals_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_user_info_function(
            self, user: str, supplied_data: dict, user_data: dict, stake: bool = False,
            block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        token_info = supplied_data['token_info']
        user_info = {}
        for lp_token, value in lp_token_info.items():
            query_id = f'balanceOf_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            decimals = user_data.get(f'decimals_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower())
            user_info[lp_token] = {
                "amount": user_data.get(query_id) / 10 ** decimals,
            }
        result = self.update_token_amount_of_wallet(user_info, lp_token_info, token_info)
        return result

    def update_token_amount_of_wallet(
            self, user_info, lp_token_info: dict = None, token_info: dict = None):
        user_info_token_amount = {}
        for lp_token, value in user_info.items():
            amount = value.get("amount", 0)
            pair_info = lp_token_info.get(lp_token)
            token0 = pair_info.get("token0")
            token1 = pair_info.get("token1")
            token0_price = token_info.get(token0)['price']
            token1_price = token_info.get(token1)['price']
            lp_token_price = pair_info.get("price")
            lp_token_amount_in_usd = amount * lp_token_price

            token0_amount = lp_token_amount_in_usd / 2 / token0_price
            token1_amount = lp_token_amount_in_usd / 2 / token1_price

            user_info_token_amount[lp_token] = {
                "amount": amount,
                'amountInUSD': lp_token_amount_in_usd,
                token0: {
                    'amount': token0_amount,
                },
                token1: {
                    'amount': token1_amount,
                }
            }

        return user_info_token_amount
