import logging

from web3 import Web3

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_services import DexServices
from defi_services.constants.entities.lending_services import LendingServices
from defi_services.constants.query_constant import Query
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex_protocol_services import DexProtocolServices
from defi_services.services.nft_services import NFTServices
from defi_services.services.protocol_services import ProtocolServices
from defi_services.services.token_services import TokenServices
from defi_services.utils.convert_address import base58_to_hex
from defi_services.utils.init_services import init_services

logger = logging.getLogger("StateProcessor")


class StateProcessor:
    def __init__(self, provider_uri: str, chain_id: str):
        self.state_querier = StateQuerier(provider_uri)
        self.chain_id = chain_id
        self.services = init_services(self.state_querier, chain_id)
        self.token_service = TokenServices(self.state_querier, chain_id)
        self.nft_service = NFTServices(self.state_querier, chain_id)
        self.lending_services = LendingServices.mapping.get(chain_id)
        self.dex_services = DexServices.mapping.get(chain_id)

    def get_service_info(self):
        info = self.nft_service.get_service_info()
        info.update(self.token_service.get_service_info())
        for service, value in self.services.items():
            info.update(value.get_service_info())

        return info

    @staticmethod
    def check_address(address):
        return Web3.isAddress(address)

    @staticmethod
    def checksum_address(address):
        return Web3.toChecksumAddress(address)

    def init_rpc_call_information(
            self, wallet: str, query_id: str, entity_id: str, query_type: str, block_number: int = 'latest', **kwargs):
        queries = {}
        tokens = []
        rpc_calls = {}
        if self.check_address(entity_id):
            if Query.token_balance == query_type:
                rpc_calls.update(self.token_service.get_function_info(
                    wallet, entity_id, block_number
                ))
                tokens.append(entity_id)

            if Query.nft_balance == query_type:
                rpc_calls.update(self.nft_service.get_function_info(
                    wallet, entity_id, block_number
                ))

        if entity_id in self.services:
            entity_service = self.services.get(entity_id)
            rpc_calls.update(entity_service.get_function_info([query_type], wallet, block_number, **kwargs))
            tokens += entity_service.get_token_list()
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

    def process_decoded_data(self, query_id: str, query_type: str, wallet: str,
                             decoded_data: dict, block_number: int = 'latest', **kwargs):
        result = {
            "query_id": query_id,
            "query_type": query_type
        }
        query_value = decoded_data.get(query_id)
        for entity, entity_value in query_value.items():
            result["entity_id"] = entity
            data = None
            if self.check_address(entity):
                if Query.token_balance == query_type:
                    data = self.token_service.get_data(wallet, entity, entity_value, block_number)

                if Query.nft_balance == query_type:
                    data = self.nft_service.get_data(wallet, entity, entity_value, block_number)

            elif entity in self.lending_services:
                entity_service: ProtocolServices = self.services.get(entity)
                data = entity_service.get_data(
                    [query_type], wallet, entity_value, block_number, **kwargs)

            elif entity in self.dex_services:
                entity_service: DexProtocolServices = self.services.get(entity)
                data = entity_service.get_data([query_type], wallet, entity_value, block_number, **kwargs)
            else:
                continue
            result[query_type] = data

        return result

    def run(self, address: str, queries: list, block_number: int = 'latest',
            batch_size: int = 100, max_workers: int = 8, ignore_error=False):
        wallet = address
        if self.chain_id == Chain.tron and address and not self.check_address(address):
            wallet = base58_to_hex(address)
        all_rpc_calls = {}
        for query in queries:
            query_type = query.get("query_type")
            query_id = query.get("query_id")
            entity_id = query.get("entity_id")
            if self.chain_id == Chain.tron and query_type in Query.balance and not self.check_address(entity_id):
                entity_id = base58_to_hex(entity_id)

            query_type = query.get("query_type")
            reserves_list = query.get("reserves_list", None)
            stake = query.get('stake', None)
            number_lp= query.get('number_lp', 1)
            supplied_data = query.get('supplied_data', None)
            rpc_calls, _ = self.init_rpc_call_information(
                wallet, query_id, entity_id, query_type, block_number, reserves_list=reserves_list,
                supplied_data=supplied_data, stake=stake, number_lp= number_lp)
            all_rpc_calls.update(rpc_calls)
        result = []
        decoded_data = self.execute_rpc_calls(all_rpc_calls, batch_size, max_workers, ignore_error=ignore_error)
        for query in queries:
            query_id = query.get("query_id")
            query_type = query.get("query_type")
            reserves_list = query.get("reserves_list", None)
            supplied_data = query.get('supplied_data', None)
            number_lp= query.get('number_lp', 1)
            stake = query.get('stake', None)
            processed_data = self.process_decoded_data(
                query_id, query_type, wallet, decoded_data, block_number, reserve_info=reserves_list,
                supplied_data=supplied_data, stake=stake, number_lp=number_lp)
            result.append(processed_data)

        return result
