import logging

from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.jobs.queriers.multicall_state_querier import MulticallStateQuerier
from defi_services.utils.convert_address import base58_to_hex

logger = logging.getLogger("MulticallStateProcessor")


class MulticallStateProcessor(StateProcessor):
    def __init__(self, provider_uri: str, chain_id: str):
        super().__init__(provider_uri, chain_id)
        self.state_querier = MulticallStateQuerier(provider_uri, chain_id)