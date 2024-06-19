import logging
from typing import List

from defi_services.abis.dex.pancakeswap.pancakeswap_v2_factory_abi import PANCAKESWAP_V2_FACTORY_ABI
from defi_services.abis.dex.sushiswap.masterchef_v2_abi import SUSHISWAP_MASTERCHEF_V2_ABI
from defi_services.abis.dex.sushiswap.minichef_abi import SUSHISWAP_MINICHEF_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.blockchain.multicall_v2 import W3Multicall
from defi_services.services.dex.dex_info.sushiswap_info import SUSHISWAP_V2_ETH_INFO, SUSHISWAP_V2_FANTOM_INFO, \
    SUSHISWAP_V2_POLYGON_INFO, SUSHISWAP_V2_AVALANCHE_INFO, SUSHISWAP_V2_ARBITRUM_INFO, SUSHISWAP_V2_BSC_INFO
from defi_services.services.dex.pancakeswap_v2_service_multicall import PancakeSwapV2Services

logger = logging.getLogger("SushiSwap V2 State Service")


class SushiSwapV2Info:
    mapping = {
        Chain.ethereum: SUSHISWAP_V2_ETH_INFO,
        Chain.fantom: SUSHISWAP_V2_FANTOM_INFO,
        Chain.polygon: SUSHISWAP_V2_POLYGON_INFO,
        Chain.avalanche: SUSHISWAP_V2_AVALANCHE_INFO,
        Chain.arbitrum: SUSHISWAP_V2_ARBITRUM_INFO,
        Chain.bsc: SUSHISWAP_V2_BSC_INFO
    }


class SushiSwapV2Services(PancakeSwapV2Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__(state_service=state_service, chain_id=chain_id)

        self.pool_info = SushiSwapV2Info.mapping.get(chain_id)
        if chain_id == Chain.ethereum:
            self.masterchef_abi = SUSHISWAP_MASTERCHEF_V2_ABI
        else:
            self.masterchef_abi = SUSHISWAP_MINICHEF_ABI
        self._w3 = state_service.get_w3()
        self.factory_abi = PANCAKESWAP_V2_FACTORY_ABI

    def get_service_info(self):
        info = {
            Dex.sushi_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    # User Reward
    def get_rewards_balance_function_info(self, wallet, supplied_data, block_number: int = "latest"):
        multicall_calls: List['W3Multicall.Call'] = []

        reward_token = self.pool_info.get("reward_token")
        multicall_calls.append(W3Multicall.Call(
            address=reward_token, abi=ERC20_ABI, fn_name='decimals', block_number=block_number))

        masterchef_addr = self.pool_info.get('master_chef_address')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                multicall_calls.append(W3Multicall.Call(
                    address=masterchef_addr, abi=self.masterchef_abi,  fn_name="pendingSushi",
                    fn_paras=[pid, self._w3.to_checksum_address(wallet)], block_number=block_number))

        return multicall_calls

    def calculate_rewards_balance(self, wallet: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest") -> dict:
        reward_token = self.pool_info.get("reward_token")
        reward_decimals = decoded_data.get(f'decimals_{reward_token}_{block_number}'.lower())

        result = {}

        masterchef_addr = self.pool_info.get('master_chef_address')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                query_id = f'pendingSushi_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                result[lp_token] = {reward_token: {'amount': decoded_data.get(query_id) / 10 ** reward_decimals}}

        return result
