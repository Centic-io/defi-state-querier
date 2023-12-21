import logging

from defi_services.abis.dex.pancakeswap.pancakeswap_factory_abi import PANCAKESWAP_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.dex.spookyswap.masterchef_v2_abi import SPOOKYSWAP_MASTERCHEF_V2_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
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
        self.factory_abi = PANCAKESWAP_FACTORY_ABI

    # Get lp token info
    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        masterchef_addr = self.pool_info.get('masterchefAddress')

        rpc_calls = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            for fn_name in ["decimals", "totalSupply", "token0", "token1", "name"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

            query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf", fn_paras=[masterchef_addr],
                block_number=block_number)

            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))

                query_id = f'getFarmData_{masterchef_addr}_{pid}_{block_number}'.lower()
                rpc_calls[query_id] = self.get_masterchef_function_info(
                    fn_name="getFarmData", fn_paras=[pid], block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, decoded_data, block_number: int = "latest"):
        masterchef_addr = self.pool_info.get('masterchefAddress')

        result = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            token0 = decoded_data.get(f'token0_{lp_token}_{block_number}'.lower())
            token1 = decoded_data.get(f'token1_{lp_token}_{block_number}'.lower())
            decimals = decoded_data.get(f'decimals_{lp_token}_{block_number}'.lower())
            total_supply = decoded_data.get(f'totalSupply_{lp_token}_{block_number}'.lower()) / 10 ** decimals
            name = decoded_data.get(f'name_{lp_token}_{block_number}'.lower())

            staked_balance_query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()
            masterchef_balance = decoded_data.get(
                staked_balance_query_id) / 10 ** decimals

            result[lp_token] = {
                "total_supply": total_supply,
                "token0": token0,
                "token1": token1,
                "name": name,
                'decimals': decimals,
                "stake_balance": masterchef_balance
            }

            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                farm_data_query_id = f'getFarmData_{masterchef_addr}_{pid}_{block_number}'.lower()
                farm_data = decoded_data.get(farm_data_query_id)
                acc_boo_per_share = farm_data[0][0] / 10 ** 18
                alloc_point = farm_data[0][2]
                total_alloc_point = farm_data[1]
                rewarder_addr = farm_data[2]

                result[lp_token].update({
                    'acc_reward_per_share': acc_boo_per_share,
                    'alloc_point': alloc_point,
                    'total_alloc_point': total_alloc_point,
                    'rewarder_address': rewarder_addr,
                    'farming_pid': pid
                })

        return result

    # User Reward
    def get_rewards_balance_function_info(self, wallet, supplied_data, block_number: int = "latest"):
        rpc_calls = {}

        reward_token = self.pool_info.get("rewardToken")
        decimals_query_id = f'decimals_{reward_token}_{block_number}'.lower()
        rpc_calls[decimals_query_id] = self.state_service.get_function_info(
            address=reward_token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        masterchef_addr = self.pool_info.get('masterchefAddress')

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
        reward_token = self.pool_info.get("rewardToken")
        reward_decimals = decoded_data.get(f'decimals_{reward_token}_{block_number}'.lower())

        result = {}

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                query_id = f'pendingBOO_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                result[lp_token] = {reward_token: {'amount': decoded_data.get(query_id) / 10 ** reward_decimals}}

        return result
