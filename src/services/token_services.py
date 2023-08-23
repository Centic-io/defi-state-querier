from abis.token.erc20_abi import ERC20_ABI
from jobs.state_querier import StateQuerier


class TokenServices:
    def __init__(self, provider_uri):
        self.state_service = StateQuerier(provider_uri)

    def get_function_token_erc_20_info(self, tokens: list, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        result = {}
        for token in tokens:
            result.update(self.state_service.get_function_info(
                token, ERC20_ABI, fn_name, fn_paras, block_number
            ))
        return result

    @staticmethod
    def get_wallet_token_balance(self, token_balance: dict, token_decimals: dict, token_price: dict):
        result = {}
        for token, value in token_balance.items():
            result[token] = value * token_price.get(token, 1) / 100 * token_decimals.get(token, 8)
        return result
