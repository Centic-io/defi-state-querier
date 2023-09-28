from defi_services.abis.token.erc721_abi import ERC721_ABI
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier


class NFTServices:
    def __init__(self, state_service: StateQuerier, chain_id: str):
        self.chain_id = chain_id
        self.state_service = state_service

    def get_service_info(self):
        info = {
            "nft": {
                "chain_id": self.chain_id,
                "type": "nft"
            }
        }
        return info

    @staticmethod
    def get_data(wallet: str, token: str, decoded_data: dict, block_number: int = "latest", **kwargs):
        token_prices = kwargs.get("token_prices", {})
        balance_key = f"balanceOf_{wallet}_{token}_{block_number}".lower()
        if balance_key in decoded_data:
            balance = decoded_data.get(balance_key) or 0
            return balance * token_prices.get(token, 1)

        return None

    def get_function_info(self, wallet: str, token: str, block_number: int = "latest"):
        result = self.get_function_balance_info(wallet, token, block_number)
        return result

    def get_function_token_erc_721_info(self, tokens: list, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        result = {}
        for token in tokens:
            erc721_token = token
            if token == Token.native_token:
                erc721_token = Token.wrapped_token.get(self.chain_id)
            key = f"{fn_name}_{erc721_token}_{block_number}".lower()
            result.update({
                key: self.state_service.get_function_info(
                    erc721_token, ERC721_ABI, fn_name, fn_paras, block_number
                )
            })

        return result

    def get_function_balance_info(self, wallet: str, token: str, block_number: int = "latest"):
        balance_token = token
        if token == Token.native_token:
            balance_token = Token.wrapped_token.get(self.chain_id)
        key = f"balanceOf_{wallet}_{balance_token}_{block_number}".lower()
        return {key: self.state_service.get_function_info(balance_token, ERC721_ABI, "balanceOf", [wallet], block_number)}
