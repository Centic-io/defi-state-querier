import logging

from defi_services.constants.chain_constant import Chain
from defi_services.jobs.state_querier import StateQuerier
from defi_services.services.lending.lending_info.fantom.geist_ftm import GEIST_ETH
from defi_services.services.lending.valas_services import ValasStateService

logger = logging.getLogger("Geist Lending Pool State Service")


class GeistInfo:
    mapping = {
        Chain.fantom: GEIST_ETH
    }


class GeistStateService(ValasStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0xfa"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_geist"
        self.pool_info = GeistInfo.mapping.get(chain_id)
