from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.solana_state_querier import SolanaStateQuerier


class SolanaTokenServices:
    def __init__(self, state_service: SolanaStateQuerier, chain_id: str = "solana"):
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

    def get_function_info(self, wallet: str, token: str):
        result = self.get_function_balance_info(wallet, token)
        return result

    def get_function_balance_info(self, wallet, token):
        key = f"balanceOf_{wallet}_{token}".lower()
        if token == Token.native_token:
            params = [wallet]
            rpc_call = self.state_service.get_function_info('getBalance', params)
        else:
            params = [wallet, {"mint": token}, {"encoding": "jsonParsed"}]
            rpc_call = self.state_service.get_function_info("getTokenAccountsByOwner", params)
        return {key: rpc_call}

    @staticmethod
    def get_data(wallet, token, decoded_data, token_prices):
        key = f"balanceOf_{wallet}_{token}".lower()
        data = decoded_data.get(key)
        token_price = token_prices.get(token, 1)
        if token == Token.native_token:
            balance = data.get("value", 0) * token_price / 10**9
            return balance
        balance = 0
        for item in data.get('value'):
            balance_info = item.get('account', {}).get('data', {}).get('parsed').get('info').get('tokenAmount')
            balance += balance_info.get("uiAmount", 0) * token_price

        return balance
