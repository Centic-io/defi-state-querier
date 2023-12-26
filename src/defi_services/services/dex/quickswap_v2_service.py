import logging

from defi_services.abis.dex.uniswap.uniswap_v2_factory import UNISWAP_FACTORY_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.quickswap_info import QUICKSWAP_POLYGON_V2_INFO
from defi_services.services.dex.uniswap_v2_service import UniswapV2Services

logger = logging.getLogger("QuickSwap V2 State Service")


class QuickSwapV2Info:
    mapping = {
        Chain.polygon: QUICKSWAP_POLYGON_V2_INFO
    }


class QuickSwapV2Services(UniswapV2Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__(state_service=state_service, chain_id=chain_id)

        self.pool_info = QuickSwapV2Info.mapping.get(chain_id)
        self.factory_abi = UNISWAP_FACTORY_ABI

    def get_service_info(self):
        info = {
            Dex.quickswap_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                protocol_info": self.pool_info
            }
        }
        return info
