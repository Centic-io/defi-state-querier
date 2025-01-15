import logging

from defi_services.abis.lending.moonwell.moonwell_comptroller_abi import MOONWELL_COMPTROLLER_ABI
from defi_services.abis.lending.moonwell.moonwell_ctoken_abi import MOONWELL_CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.base.moonwell_base import MOONWELL_BASE
from defi_services.services.lending.venus_services import VenusStateService

logger = logging.getLogger("MoonWell Lending Pool State Service")


class MoonWellInfo:
    mapping = {
        Chain.base: MOONWELL_BASE
    }


class MoonWellStateService(VenusStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x38"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.venus}"
        self.chain_id = chain_id
        self.pool_info = MoonWellInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.comptroller_abi = MOONWELL_COMPTROLLER_ABI
        self.vtoken_abi = MOONWELL_CTOKEN_ABI

    def get_service_info(self):
        info = {
            Lending.moonwell: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, reserve_info in reserves_info.items():
            if token_address != Token.native_token:
                query_id = f"decimals_{token_address}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(token_address, ERC20_ABI, "decimals", [], block_number)

            ctoken = reserve_info.get("cToken")
            for fn_name in ['decimals', 'totalSupply', 'totalBorrows', 'supplyRatePerTimestamp', 'borrowRatePerTimestamp', 'exchangeRateStored']:
                query_id = f"{fn_name}_{ctoken}_{block_number}".lower()
                rpc_calls[query_id] = self.get_ctoken_function_info(
                    ctoken=ctoken,
                    fn_name=fn_name,
                    block_number=block_number
                )

        return rpc_calls

    def get_reserve_tokens_metadata(
            self,
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token_address, reserve_info in reserves_info.items():
            if token_address != Token.native_token:
                underlying_decimals_query_id = f"decimals_{token_address}_{block_number}".lower()
                underlying_decimals = decoded_data.get(underlying_decimals_query_id)
            else:
                underlying_decimals = Chain.native_decimals.get(self.chain_id, 18)

            ctoken = reserve_info.get("cToken")
            ctoken_decimals_query_id = f"decimals_{ctoken}_{block_number}".lower()
            total_supply_query_id = f"totalSupply_{ctoken}_{block_number}".lower()
            total_borrow_query_id = f"totalBorrows_{ctoken}_{block_number}".lower()
            supply_rate_query_id = f"supplyRatePerTimestamp_{ctoken}_{block_number}".lower()
            borrow_rate_query_id = f"borrowRatePerTimestamp_{ctoken}_{block_number}".lower()
            exchange_rate_query_id = f"exchangeRateStored_{ctoken}_{block_number}".lower()

            reserve_tokens_info.append({
                "token": ctoken,
                "token_decimals": decoded_data.get(ctoken_decimals_query_id),
                "borrow_rate": decoded_data.get(borrow_rate_query_id),
                "supply_rate": decoded_data.get(supply_rate_query_id),
                "supply": decoded_data.get(total_supply_query_id),
                "borrow": decoded_data.get(total_borrow_query_id),
                "exchange_rate": decoded_data.get(exchange_rate_query_id),
                "underlying_decimals": underlying_decimals,
                "underlying": token_address
            })
        return reserve_tokens_info

    @classmethod
    def _calculate_interest_rates(
            cls, token_info: dict, pool_decimals: int, apx_block_speed_in_seconds: float):
        exchange_rate = float(token_info["exchange_rate"]) / 10 ** (18 - 8 + token_info["underlying_decimals"])

        total_borrow = float(token_info["borrow"]) / 10 ** int(token_info["underlying_decimals"])
        total_supply = float(token_info["supply"]) * exchange_rate / 10 ** int(token_info["token_decimals"])

        supply_apy = ((token_info["supply_rate"] / 10 ** pool_decimals) * 86400 + 1) ** 365 - 1
        borrow_apy = ((token_info["borrow_rate"] / 10 ** pool_decimals) * 86400 + 1) ** 365 - 1

        return {
            'deposit_apy': supply_apy,
            'borrow_apy': borrow_apy,
            'total_deposit': total_supply,
            'total_borrow': total_borrow
        }

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, self.vtoken_abi, fn_name, fn_paras, block_number
        )
