from defi_services.constants.cosmos_decimals_constant import Denoms, MulticallContract
from defi_services.constants.network_constants import Chains
from defi_services.services.cosmos_token_services import CosmosTokenServices


class CosmosStateProcessor:
    def __init__(self, lcd: str, rest_uri: str = None, chain_id: str = Chains.oraichain):
        self.chain_id = chain_id
        self.lcd = lcd
        self.rest_uri = rest_uri

    def get_token_balance(self, address, tokens):
        cosmos = CosmosTokenServices(self.lcd, self.rest_uri, self.chain_id)
        if self.chain_id in MulticallContract.mapping:
            data = cosmos.query_balances(address, tokens)
        else:
            result = cosmos.query_coin_balances(address=address)
            data = {}
            for item in result:
                denom = item.get('denom', "").lower()
                amount = int(item.get('amount', None))
                decimal = Denoms.all.get(denom, {}).get("decimal", 0)
                data[denom] = amount / 10 ** decimal

        return data

    def run(self, address: str, queries: list):
        result = []
        tokens = [query.get('entity_id').lower() for query in queries if query.get('query_type') == 'token_balance']
        token_balances = self.get_token_balance(address, tokens)
        for query in queries:
            query_id = query.get("query_id")
            entity_id = query.get("entity_id")
            query_type = query.get("query_type")
            if query_type != "token_balance":
                continue

            result.append(
                {"query_id": query_id,
                 "query_type": query_type,
                 "entity_id": entity_id,
                 "token_balance": token_balances.get(entity_id, 0)
                 })
        return result
