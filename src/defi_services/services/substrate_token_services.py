from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.substrate_state_querier import SubstrateStateQuerier


class SubstrateTokenServices:
    def __init__(self, state_service: SubstrateStateQuerier, chain_id: str = "polkadot"):
        self.chain_id = chain_id
        self.state_service = state_service
        self.token_info = self.get_assets()

    def get_assets(self):
        if self.chain_id in ['polkadot']:
            return {}
        client_querier = self.state_service.get_client_querier()
        assets = client_querier.query_map("Assets", "Metadata")
        result = {}
        for asset in assets.records:
            token_id = str(asset[0].value)
            result[token_id] = asset[1].value_serialized

        return result

    def get_service_info(self):
        info = {
            "token": {
                "chain_id": self.chain_id,
                "type": "token"
            }
        }
        return info

    def get_function_info(self, wallet: str, token: str, block_number: int = "latest"):
        result = self.get_function_balance_info(wallet, token, block_number)

        return result

    def get_function_balance_info(self, wallet: str, token: str = None, block_number: int = "latest"):
        if not token or token == Token.native_token:
            key = f"System_Account_{[wallet]}_{block_number}".lower()
            rpc_call = self.state_service.get_function_info("System", "Account", [wallet], block_number)
        else:
            token = int(token)
            params = [int(token), wallet]
            key = f"Assets_Account_{params}_{block_number}".lower()
            rpc_call = self.state_service.get_function_info("Assets", "Account", params, block_number)

        return {key: rpc_call}

    def get_asset_info(self, token: str):
        token = int(token)
        key = f"Assets_Asset_{token}".lower()
        rpc_call = self.state_service.get_function_info("Assets", "Asset", [token])
        return {key, rpc_call}

    def get_data(self, wallet: str, token: str = None, decoded_data: dict = None,
                 token_prices: dict = None, block_number: int = "latest"):
        if not token or token == Token.native_token:
            key = f"System_Account_{[wallet]}_{block_number}".lower()
            balance = decoded_data.get(key).get('data').get("free") / 10 ** 10
        else:
            if token not in self.token_info:
                self.token_info = self.get_assets()
            token_decimals = self.token_info.get(token, {}).get('decimals', 0)
            token = int(token)
            params = [int(token), wallet]
            key = f"Assets_Account_{params}_{block_number}".lower()
            balance = decoded_data.get(key).get("balance") / 10 ** token_decimals
        token_price = token_prices.get(token, 1)
        balance = balance * token_price
        return balance
