import logging

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v3_services import AaveV3StateService
from defi_services.services.lending.lending_info.base.zerolend_base import ZEROLEND_BASE
from defi_services.services.lending.lending_info.ethereum.zerolend_eth import ZEROLEND_ETH
from defi_services.services.lending.lending_info.zksync.zerolend_zksync import ZEROLEND_ZKSYNC

logger = logging.getLogger("ZeroLend Lending Pool State Service")


class ZeroLendInfo:
    mapping = {
        Chain.zksync: ZEROLEND_ZKSYNC,
        Chain.ethereum: ZEROLEND_ETH,
        Chain.base: ZEROLEND_BASE
    }


class ZeroLendStateService(AaveV3StateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = Chain.zksync):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.zerolend}"
        self.pool_info = ZeroLendInfo.mapping.get(chain_id)

    def get_service_info(self):
        info = {
            Lending.zerolend: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info