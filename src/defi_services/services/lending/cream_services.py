import logging

from web3 import Web3

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.bsc.cream_bsc import CREAM_BSC

logger = logging.getLogger("Cream Lending Pool State Service")


class CreamInfo:
    mapping = {
        Chain.bsc: CREAM_BSC
    }


class CreamStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.cream}"
        self.chain_id = chain_id
        self.pool_info = CreamInfo.mapping.get(chain_id)

    def get_service_info(self):
        info = {
            Lending.cream: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        token = self.pool_info.get("poolToken")
        fn_paras = [Web3.toChecksumAddress(token),
                    Web3.toChecksumAddress(self.pool_info.get("comptrollerImplementationAddress")),
                    Web3.toChecksumAddress(wallet_address)]
        rpc_call = self.get_lens_function_info("getCompBalanceMetadataExt", fn_paras, block_number)
        get_reward_id = f"getCompBalanceMetadataExt_{self.name}_{wallet_address}_{block_number}".lower()
        return {get_reward_id: rpc_call}

