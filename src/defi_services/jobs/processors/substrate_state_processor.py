import logging

from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.jobs.queriers.substrate_state_querier import SubstrateStateQuerier
from defi_services.services.substrate_token_services import SubstrateTokenServices

logger = logging.getLogger("SubstrateStateProcessor")


class SubstrateStateProcessor:
    def __init__(self, provider_uri: str, chain_id: str):
        self.state_querier = SubstrateStateQuerier(provider_uri)
        self.chain_id = chain_id
        self.token_service = SubstrateTokenServices(self.state_querier, chain_id)

    def get_service_info(self):
        info = self.token_service.get_service_info()
        return info

    def init_rpc_call_information(
            self, wallet: str, query_id: str, entity_id: str, query_type: str, block_number: int = 'latest'):
        queries = {}
        tokens = []
        rpc_calls = {}
        if entity_id not in Lending.all and query_type in [Query.token_balance, Query.nft_balance]:
            rpc_calls.update(self.token_service.get_function_info(wallet, entity_id, block_number))
            tokens.append(entity_id)

        queries[entity_id] = rpc_calls
        tokens = list(set(tokens))
        return {query_id: queries}, tokens

    def execute_rpc_calls(self, queries: dict, batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False):
        rpc_calls = {}
        for query, query_info in queries.items():
            for entity, entity_value in query_info.items():
                rpc_calls.update(entity_value)

        decoded_data = self.state_querier.query_state_data(
            rpc_calls, batch_size=batch_size, workers=max_workers, ignore_error=ignore_error)
        result = {}
        for query, query_info in queries.items():
            query_data = {}
            for entity, entity_value in query_info.items():
                entity_data = {}
                for key, value in entity_value.items():
                    entity_data[key] = decoded_data.get(key)
                query_data[entity] = entity_data
            result[query] = query_data

        return result

    def process_decoded_data(
            self, query_id: str, query_type: str, wallet: str,
            token_prices: dict, decoded_data: dict):
        result = {
            "query_id": query_id,
            "query_type": query_type
        }
        query_value = decoded_data.get(query_id)
        for entity, entity_value in query_value.items():
            result["entity_id"] = entity
            data = None
            if entity not in Lending.all and query_type in [Query.nft_balance, Query.token_balance]:
                data = self.token_service.get_data(wallet, entity, entity_value, token_prices)
            result[query_type] = data

        return result

    def run(self, address: str, queries: list, block_number: int = 'latest',
            batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False, token_prices: dict = None):
        all_rpc_calls = {}
        for query in queries:
            query_id = query.get("query_id")
            entity_id = query.get("entity_id")
            query_type = query.get("query_type")
            rpc_calls, _ = self.init_rpc_call_information(
                address, query_id, entity_id, query_type, block_number)
            all_rpc_calls.update(rpc_calls)
        result = []
        decoded_data = self.execute_rpc_calls(all_rpc_calls, batch_size, max_workers, ignore_error=ignore_error)
        if token_prices is None:
            token_prices = {}
        for query in queries:
            query_id = query.get("query_id")
            query_type = query.get("query_type")
            processed_data = self.process_decoded_data(
                query_id, query_type, address, token_prices, decoded_data)
            result.append(processed_data)

        return result
