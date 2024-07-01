import logging

from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.jobs.queriers.call_state_querier import CallStateQuerier

logger = logging.getLogger("CallStateProcessor")


class CallStateProcessor(StateProcessor):
    def __init__(self, provider_uri: str, chain_id: str):
        super().__init__(provider_uri, chain_id)
        self.state_querier = CallStateQuerier(provider_uri, chain_id)
