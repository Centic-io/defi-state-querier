import logging

from defi_services.abis.lending.radiant_v2.radiant_v2_incentive_abi import RADIANT_V2_INCENTIVE_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.arbitrum.radiant_arbitrum import RADIANT_ARB
from defi_services.services.lending.lending_info.bsc.radiant_bsc import RADIANT_BSC
from defi_services.services.lending.valas_services import ValasStateService
from defi_services.utils.apy import apr_to_apy

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
        self.incentive_abi = RADIANT_V2_INCENTIVE_ABI

    def get_service_info(self):
        info = {
            Lending.radiant_v2: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    # PROTOCOL APY
    @classmethod
    def _calculate_interest_rates(cls, token_info: dict):
        total_supply_t = token_info.get('a_token_supply')
        total_supply_d = token_info.get('d_token_supply')

        total_supply = total_supply_t / 10 ** token_info['underlying_decimals']
        total_borrow = total_supply_d / 10 ** token_info['underlying_decimals']

        supply_apr = float(token_info['supply_apy']) / 10 ** 27
        supply_apy = apr_to_apy(supply_apr)
        borrow_apr = float(token_info['borrow_apy']) / 10 ** 27
        borrow_apy = apr_to_apy(borrow_apr)

        return {
            DBConst.deposit_apy: supply_apy,
            DBConst.borrow_apy: borrow_apy,
            DBConst.total_deposit: total_supply,
            DBConst.total_borrow: total_borrow
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        key = f"allPendingRewards_{self.name}_{wallet}_{block_number}".lower()
        rpc_calls[key] = self.get_function_incentive_info(
            "allPendingRewards", [wallet], block_number)

        return rpc_calls

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        reward_token = self.pool_info['rewardToken']
        key = f"allPendingRewards_{self.name}_{wallet}_{block_number}".lower()
        rewards = decoded_data.get(key) / 10 ** 18
        result = {
            reward_token: {"amount": rewards}
        }

        return result
