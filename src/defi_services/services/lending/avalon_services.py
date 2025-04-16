import logging

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v3_services import AaveV3StateService
from defi_services.services.lending.lending_info.bsc.avalon_bsc import AVALON_BSC

logger = logging.getLogger("Avalon Lending Pool State Service")


class AvalonInfo:
    mapping = {
        Chain.bsc: AVALON_BSC
    }


class AvalonStateService(AaveV3StateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x38"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.avalon}"
        self.chain_id = chain_id
        self.pool_info = AvalonInfo.mapping.get(chain_id)
        self.state_service = state_service

    def get_service_info(self):
        info = {
            Lending.avalon: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info
