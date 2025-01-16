import logging

from defi_services.abis.lending.venus.venus_comptroller_abi import VENUS_COMPTROLLER_ABI
from defi_services.abis.lending.venus.vtoken_abi import VTOKEN_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.base.sonne_base import SONNE_BASE
from defi_services.services.lending.venus_services import VenusStateService

logger = logging.getLogger("Ionic Lending Pool State Service")


class SonneInfo:
    mapping = {
        Chain.base: SONNE_BASE
    }


class SonneStateService(VenusStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x38"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.sonne}"
        self.chain_id = chain_id
        self.pool_info = SonneInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.comptroller_abi = VENUS_COMPTROLLER_ABI
        self.vtoken_abi = VTOKEN_ABI

    def get_service_info(self):
        info = {
            Lending.sonne: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = "latest",
    ):
        reserve_tokens_info = self.get_reserve_tokens_metadata(decoded_data, reserves_info, block_number)

        data = {}
        for token_info in reserve_tokens_info:
            underlying_token = token_info['underlying']
            c_token = token_info['token']

            assets = {
                underlying_token: self._calculate_interest_rates(
                    token_info, pool_decimals=pool_decimals,
                    apx_block_speed_in_seconds=1
                )
            }
            data[c_token] = assets

        return data
