import logging

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v3_services import AaveV3StateService
from defi_services.services.lending.lending_info.ethereum.spark_eth import SPARK_ETH

logger = logging.getLogger("Spark Lending Pool State Service")


class SparkInfo:
    mapping = {
        Chain.ethereum: SPARK_ETH
    }


class SparkStateService(AaveV3StateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.spark}"
        self.pool_info = SparkInfo.mapping.get(chain_id)

    def get_service_info(self):
        info = {
            Lending.spark: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info
