import logging

from defi_services.abis.dex.pancakeswap.pancakeswap_v2_factory_abi import PANCAKESWAP_V2_FACTORY_ABI
from defi_services.abis.dex.spookyswap.masterchef_v2_abi import SPOOKYSWAP_MASTERCHEF_V2_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.spookyswap_info import SPOOKY_FTM_V2_INFO
from defi_services.services.dex.pancakeswap_v2_service import PancakeSwapV2Services

logger = logging.getLogger("Spooky V2 State Service")


class SpookySwapV2Info:
    mapping = {
        Chain.fantom: SPOOKY_FTM_V2_INFO
    }


class SpookySwapV2Services(PancakeSwapV2Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0xfa'):
        super().__init__(state_service=state_service, chain_id=chain_id)

        self.pool_info = SpookySwapV2Info.mapping.get(chain_id)

        self.masterchef_abi = SPOOKYSWAP_MASTERCHEF_V2_ABI
        self.factory_abi = PANCAKESWAP_V2_FACTORY_ABI

    def get_service_info(self):
        info = {
            Dex.spooky_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    # User Reward
    def get_rewards_balance_function_info(self, wallet, supplied_data, block_number: int = "latest"):
        rpc_calls = {}

        reward_token = self.pool_info.get("reward_token")
        decimals_query_id = f'decimals_{reward_token}_{block_number}'.lower()
        rpc_calls[decimals_query_id] = self.state_service.get_function_info(
            address=reward_token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        masterchef_addr = self.pool_info.get('master_chef_address')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))

                query_id = f'pendingBOO_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()
                rpc_calls[query_id] = self.get_masterchef_function_info(
                    fn_name="pendingBOO", fn_paras=[int(pid), wallet], block_number=block_number)

        return rpc_calls

    def calculate_rewards_balance(self, wallet: str, supplied_data: dict, decoded_data: dict,
                                  block_number: int = "latest") -> dict:
        reward_token = self.pool_info.get("reward_token")
        reward_decimals = decoded_data.get(f'decimals_{reward_token}_{block_number}'.lower())

        result = {}

        masterchef_addr = self.pool_info.get('master_chef_address')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                query_id = f'pendingBOO_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                result[lp_token] = {reward_token: {'amount': decoded_data.get(query_id) / 10 ** reward_decimals}}

        return result
