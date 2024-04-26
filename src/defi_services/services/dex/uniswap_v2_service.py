import logging

from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.uniswap_info import UNISWAP_ETH_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("UniSwap V2 State Service")


class UniswapV2Info:
    mapping = {
        Chain.ethereum: UNISWAP_ETH_INFO
    }


class UniswapV2Services(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = UniswapV2Info.mapping.get(chain_id)
        if self.pool_info:
            self.factory_abi = self.pool_info['factory_abi']

    def get_service_info(self):
        info = {
            Dex.uniswap_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit=10000, supplied_data: dict = None):
        web3 = self.state_service.get_w3()
        factory_addr = self.pool_info.get('factory_address')

        factory_contract = web3.eth.contract(
            address=web3.to_checksum_address(factory_addr), abi=self.factory_abi)
        pool_length = factory_contract.functions.allPairsLength().call()

        rpc_calls = {}
        for pid in range(0, min(pool_length, limit)):
            query_id = f'allPairs_{factory_addr}_{pid}_latest'.lower()
            rpc_calls[query_id] = self.get_factory_function_info(fn_name="allPairs", fn_paras=[pid])

        return rpc_calls

    def decode_all_supported_lp_token(self, limit: int = 10, decoded_data: dict = None,
                                      supplied_data: dict = None):
        result = {}
        for query_id, value in decoded_data.items():
            # Format query_id: f'allPairs_{self.factory_addr}_{pid}_latest'

            pid = int(query_id.split("_")[-2])
            result[value.lower()] = {"pid": pid}

        return result

    def get_farming_supported_lp_token(self, limit: int = 10) -> dict:
        return {}

    def decode_farming_supported_lp_token(self, response_data) -> dict:
        return {}

    def get_important_lp_token(self, supplied_data, block_number: int = "latest"):
        """Deprecated"""
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
        """Deprecated"""
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

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            for fn_name in ["decimals", "totalSupply", "token0", "token1", "name"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, decoded_data, block_number: int = "latest"):

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            try:
                token0 = decoded_data.get(f'token0_{lp_token}_{block_number}'.lower())
                token1 = decoded_data.get(f'token1_{lp_token}_{block_number}'.lower())
                decimals = decoded_data.get(f'decimals_{lp_token}_{block_number}'.lower())
                if (not token0) and (not token1) and (decimals is None):
                    continue

                total_supply = decoded_data.get(f'totalSupply_{lp_token}_{block_number}'.lower()) / 10 ** decimals
                name = decoded_data.get(f'name_{lp_token}_{block_number}'.lower())

                lp_token_info[lp_token].update({
                    "total_supply": total_supply,
                    "token0": token0,
                    "token1": token1,
                    "name": name,
                    'decimals': decimals
                })
            except Exception:
                continue
        return lp_token_info

    # Get balance of token
    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            for token_key in ["token0", "token1"]:
                token_address = info.get(token_key, None)
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

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            try:
                for token_key in ["token0", "token1"]:
                    token_address = info.get(token_key, None)
                    query_id = f'balanceOf_{token_address}_{lp_token}_{block_number}'.lower()

                    if (token_address is not None) and (decoded_data.get(query_id) is not None):
                        token_decimals = decoded_data.get(f'decimals_{token_address}_{block_number}'.lower()) or 18
                        lp_token_info[lp_token][f'{token_key}_amount'] = decoded_data.get(
                            query_id) / 10 ** token_decimals
            except Exception:
                continue
        return lp_token_info

    # User
    def get_user_info_function(self, wallet: str, supplied_data, stake: bool = False, block_number: int = "latest"):
        rpc_calls = {}

        lp_token_info = supplied_data['lp_token_info']
        # lượng token đang hold trong ví
        for lp_token, value in lp_token_info.items():
            query_id = f'balanceOf_{lp_token}_{wallet}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf",
                fn_paras=[wallet], block_number=block_number)

            decimals_query_id = f'decimals_{lp_token}_{block_number}'.lower()
            rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_user_info_function(
            self, wallet: str, supplied_data: dict, decoded_data: dict, stake: bool = False,
            block_number: int = "latest"):

        result = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            try:
                query_id = f'balanceOf_{lp_token}_{wallet}_{block_number}'.lower()
                decimals = decoded_data.get(f'decimals_{lp_token}_{block_number}'.lower())
                amount = decoded_data.get(query_id) / 10 ** decimals

                total_supply = info.get('total_supply')

                result[lp_token] = {
                    "amount": amount,
                    "tokens": {
                        info['token0']: {
                            'idx': 0,
                            'amount': amount * info.get('token0_amount', 0) / total_supply if total_supply else 0
                        },
                        info['token1']: {
                            'idx': 1,
                            'amount': amount * info.get('token1_amount', 0) / total_supply if total_supply else 0
                        }
                    }
                }
            except Exception:
                continue

        return result

    def get_rewards_balance_function_info(self, wallet, supplied_data, block_number: int = "latest"):
        return {}

    def calculate_rewards_balance(
            self, wallet: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest") -> dict:
        return {}

    def get_factory_function_info(self, fn_name, fn_paras, block_number: int = 'latest'):
        factory_addr = self.pool_info.get('factory_address')
        return self.state_service.get_function_info(
            factory_addr, self.factory_abi, fn_name, fn_paras, block_number
        )
