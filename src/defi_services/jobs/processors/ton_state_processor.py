import logging

from defi_services.constants.ton_decimals_constant import TonTokens
from defi_services.constants.network_constants import Chains, NATIVE_TOKENS
from defi_services.jobs.queriers.ton_state_querier import TonStateQuerier

logger = logging.getLogger("CosmosStateProcessor")

class TonStateProcessor:
    def __init__(self, provider_uri: str, chain_id: str = Chains.ton):
        self.chain_id = chain_id
        self.provider_uri = provider_uri
        self.state_querier = TonStateQuerier(self.provider_uri)


    def get_token_balance(self, address, tokens):
        result = {}
        if NATIVE_TOKENS[self.chain_id] in tokens:
            native_response = self.state_querier.query_ton_coin_balances(address)
            native_balance = native_response.get("result", 0)
            result[NATIVE_TOKENS[self.chain_id]] = float(native_balance) / 10**9

        response = self.state_querier.query_jetton_coin_balances(address)
        for token_balance in response:
            jetton = token_balance.get('jetton').lower()[2:]
            if jetton not in TonTokens.mapping:
                continue
            token_address = TonTokens.mapping.get(jetton).get("address")
            if token_address not in tokens:
                continue
            decimals = TonTokens.mapping.get(jetton).get("decimals")
            balance = token_balance.get('balance', 0)
            result[token_address] = float(balance) / 10**decimals

        return result

    def run(self, address: str, queries: list, *args, **kwargs):
        result = []
        tokens = [query.get('entity_id') for query in queries if query.get('query_type') == 'token_balance']
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
