import logging

from defi_services.jobs.processors.multi_state_processor import MultiStateProcessor
from defi_services.jobs.queriers.call_state_querier import CallStateQuerier

logger = logging.getLogger("MultiCallStateProcessor")


class MultiCallStateProcessor(MultiStateProcessor):
    def __init__(self, provider_uri: str, chain_id: str):
        super().__init__(provider_uri, chain_id)
        self.state_querier = CallStateQuerier(provider_uri, chain_id)
