from defi_services.constants.cosmos_decimals_constant import Denoms
from defi_services.services.cosmos_token_services import CosmosTokenServices


class CosmosStateProcessor:
    def __init__(self, lcd: str, denom: str):
        self.lcd = lcd
        self.denom = denom

    def get_token_balance(self, address):
        cosmos = CosmosTokenServices(self.lcd, self.denom)
        data = cosmos.query_balances(address)
        result = {}
        for item in data:
            denom = item.get('denom', "").lower()
            amount = int(item.get('amount', None))
            decimal = Denoms.data.get(denom, {}).get("decimal", 0)
            result[denom] = amount / 10 ** decimal
        return result

    def run(self, address: str, queries: list):
        result = []
        token_balances = self.get_token_balance(address)
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
