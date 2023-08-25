from web3 import Web3

from constants.entities.lending import Lending
from constants.query_constant import Query
from database.mongodb import MongoDB
from jobs.state_querier import StateQuerier
from services.protocol_services import ProtocolServices
from services.token_services import TokenServices
from utils.init_services import init_services


class StateProcessor:
    def __init__(self, provider_uri: str, chain_id: str, mongodb: MongoDB = None):
        self.mongodb = mongodb
        self.state_querier = StateQuerier(provider_uri)
        self.chain_id = chain_id
        self.services = init_services(self.state_querier, chain_id)
        self.token_service = TokenServices(self.state_querier, chain_id)
        self.lending_services = Lending.mapping.get(chain_id)

    @staticmethod
    def check_address(address):
        return Web3.isAddress(address)

    @staticmethod
    def checksum_address(address):
        return Web3.toChecksumAddress(address)

    def get_token_prices(self, tokens):
        return self.mongodb.get_token_prices(tokens, self.chain_id)

    def init_rpc_call_information(
            self, wallet: str, query_id: str, entity_id: str, query_type: str, block_number: int = 'latest',
            **kwargs):
        queries = {}
        tokens = []
        rpc_calls = {}
        if self.check_address(entity_id) and Query.token_balance == query_type:
            rpc_calls.update(self.token_service.get_function_info(
                wallet, entity_id, block_number
            ))
            tokens.append(entity_id)

        if entity_id in self.services:
            entity_service: ProtocolServices = self.services.get(entity_id)
            rpc_calls.update(entity_service.get_function_info([query_type], wallet, block_number, **kwargs))
            tokens += entity_service.get_token_list()
        queries[entity_id] = rpc_calls
        tokens = list(set(tokens))
        return {query_id: queries}, tokens

    def execute_rpc_calls(self, queries: dict, batch_size: int = 100, max_workers: int = 8):
        rpc_calls = {}
        for query, query_info in queries.items():
            for entity, entity_value in query_info.items():
                rpc_calls.update(entity_value)

        decoded_data = self.state_querier.query_state_data(
            rpc_calls, batch_size=batch_size, workers=max_workers)
        result = {}
        for query, query_info in queries.items():
            query_data = {}
            for entity, entity_value in query_info.items():
                entity_data = {}
                for key, value in entity_value.items():
                    entity_data[key] = decoded_data[key]
                query_data[entity] = entity_data
            result[query] = query_data

        return result

    def process_decoded_data(
            self, query_id: str, query_type: str, wallet: str,
            token_prices: dict, decoded_data: dict, block_number: int = 'latest'):
        result = {
            "query_id": query_id,
            "query_type": query_type
        }
        query_value = decoded_data.get(query_id)
        for entity, entity_value in query_value.items():
            result["entity_id"] = entity
            if self.check_address(entity):
                data = self.token_service.get_data(wallet, entity, entity_value, token_prices, block_number)

            elif entity in self.lending_services:
                entity_service: ProtocolServices = self.services.get(entity)
                data = entity_service.get_data(
                    [query_type], wallet, entity_value, block_number, token_prices=token_prices)
            else:
                continue
            result[query_type] = data

        return result

    def run(self, wallet: str, queries: list, block_number: int = 'latest', batch_size: int = 100, max_workers: int = 8):
        all_rpc_calls, all_tokens = {}, []
        for query in queries:
            query_id = query.get("query_id")
            entity_id = query.get("entity_id")
            query_type = query.get("query_type")
            rpc_calls, tokens = self.init_rpc_call_information(
                wallet, query_id, entity_id, query_type, block_number)
            all_rpc_calls.update(rpc_calls)
            all_tokens += tokens
        result = []
        decoded_data = self.execute_rpc_calls(all_rpc_calls, batch_size, max_workers)
        token_prices = {}
        if self.mongodb:
            token_prices = self.get_token_prices(all_tokens)
        for query in queries:
            query_id = query.get("query_id")
            query_type = query.get("query_type")
            processed_data = self.process_decoded_data(
                query_id, query_type, wallet, token_prices, decoded_data, block_number)
            result.append(processed_data)

        return result





