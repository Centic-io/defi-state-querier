from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.token_constant import Token
from defi_services.jobs.state_querier import StateQuerier


class TokenServices:
    def __init__(self, state_service: StateQuerier, chain_id: str):
        self.chain_id = chain_id
        self.state_service = state_service

    def get_service_info(self):
        info = {
            "token": {
                "chain_id": self.chain_id,
                "type": "token"
            }
        }
        return info

    @staticmethod
    def get_data(wallet: str, token: str, decoded_data: dict, token_price: dict, block_number: int = "latest"):
        decimals_key = f"decimals_{token}_{block_number}".lower()
        balance_key = f"balanceOf_{wallet}_{token}_{block_number}".lower()
        if balance_key in decoded_data:
            balance = decoded_data.get(balance_key) or 0
            decimals = decoded_data.get(decimals_key, 18)
            return balance * token_price.get(token, 1) / 10 ** decimals

        return None

    def get_function_info(self, wallet: str, token: str, block_number: int = "latest"):
        result = self.get_function_balance_info(wallet, token, block_number)
        result.update(self.get_decimals_info(token, block_number))
        return result

    def get_function_token_erc_20_info(self, tokens: list, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        result = {}
        for token in tokens:
            erc20_token = token
            if token == Token.native_token:
                erc20_token = Token.wrapped_token.get(self.chain_id)
            key = f"{fn_name}_{erc20_token}_{block_number}".lower()
            result.update({
                key: self.state_service.get_function_info(
                    erc20_token, ERC20_ABI, fn_name, fn_paras, block_number
                )
            })

        return result

    def get_function_balance_info(self, wallet: str, token: str, block_number: int = "latest"):
        balance_token = token
        if token == Token.native_token:
            balance_token = Token.wrapped_token.get(self.chain_id)
        key = f"balanceOf_{wallet}_{balance_token}_{block_number}".lower()
        return {key: self.state_service.get_function_info(balance_token, ERC20_ABI, "balanceOf", [wallet], block_number)}

    def get_decimals_info(self, token: str, block_number: int = "latest"):
        decimals_token = token
        if token == Token.native_token:
            decimals_token = Token.wrapped_token.get(self.chain_id)
        key = f"decimals_{decimals_token}_{block_number}".lower()
        return {key: self.state_service.get_function_info(decimals_token, ERC20_ABI, "decimals", [], block_number)}
