import logging

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.state_querier import StateQuerier
from defi_services.services.lending.lending_info.arbitrum.radiant_arbitrum import RADIANT_ARB
from defi_services.services.lending.lending_info.bsc.radiant_bsc import RADIANT_BSC
from defi_services.services.lending.valas_services import ValasStateService

logger = logging.getLogger("Radiant Lending Pool State Service")


class RadiantInfo:
    mapping = {
        Chain.arbitrum: RADIANT_ARB,
        Chain.bsc: RADIANT_BSC
    }


class RadiantStateService(ValasStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0xa4b1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.radiant_v2}"
        self.pool_info = RadiantInfo.mapping.get(chain_id)

    def get_service_info(self):
        info = {
            Lending.radiant_v2: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info
