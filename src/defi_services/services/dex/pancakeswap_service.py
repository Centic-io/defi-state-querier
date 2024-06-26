import logging

from defi_services.abis.dex.pancakeswap.masterchef_v0_abi import PANCAKESWAP_MASTERCHEF_V0_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.pancakeswap_info import PANCAKESWAP_V0_BSC_INFO
from defi_services.services.dex.pancakeswap_v2_service import PancakeSwapV2Services

logger = logging.getLogger("PancakeSwap Staking V1 Pool State Service")


class PancakeSwapInfo:
    mapping = {
        Chain.bsc: PANCAKESWAP_V0_BSC_INFO
    }


class PancakeSwapServices(PancakeSwapV2Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__(state_service=state_service, chain_id=chain_id)

        self.pool_info = PancakeSwapInfo.mapping.get(chain_id)
        self.masterchef_abi = PANCAKESWAP_MASTERCHEF_V0_ABI

    def get_service_info(self):
        info = {
            Dex.pancake: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_farming_supported_lp_token(self, limit: int = 1):
        web3 = self.state_service.get_w3()
        masterchef_addr = self.pool_info.get('master_chef_address')

        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi,
                                                 address=web3.to_checksum_address(masterchef_addr))
        pool_length = master_chef_contract.functions.poolLength().call()

        rpc_calls = {}
        for pid in range(0, min(pool_length, limit)):
            query_id = f'lpToken_{masterchef_addr}_{pid}_latest'.lower()
            rpc_calls[query_id] = self.get_masterchef_function_info(fn_name="poolInfo", fn_paras=[pid])

        return rpc_calls

    def decode_farming_supported_lp_token(self, decoded_data):
        result = {}
        for query_id, value in decoded_data.items():
            # Format query_id: f'poolInfo_{self.masterchef_addr}_{pid}_latest'

            lp_token = value[0].lower()
            pid = int(query_id.split("_")[-2])
            result[lp_token] = {"farming_pid": pid}

        return result

    # User Information
    def get_user_info_function(
            self, wallet: str, supplied_data, stake: bool = True, block_number: int = "latest"):
        masterchef_addr = self.pool_info.get('master_chef_address')

        rpc_calls = {}

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if stake and (info.get('farming_pid') is not None):
                pid = int(info.get('farming_pid'))

                query_id = f'userInfo_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()
                rpc_calls[query_id] = self.get_masterchef_function_info(
                    fn_name="userInfo", fn_paras=[pid, wallet], block_number=block_number)

        return rpc_calls

    def decode_user_info_function(
            self, wallet: str, supplied_data, decoded_data: dict, stake: bool = True, block_number: int = "latest"):

        result = {}

        masterchef_addr = self.pool_info.get('master_chef_address')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if stake and (info.get('farming_pid') is not None):
                pid = int(info.get('farming_pid'))
                query_id = f'userInfo_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                user_info = decoded_data.get(query_id)
                stake_amount = user_info[0] / 10 ** info.get('decimals', 18) if user_info else 0

                total_supply = info.get('total_supply')

                result[lp_token] = {
                    'farming_pid': pid,
                    'stake_amount': stake_amount,
                    'tokens': {
                        info['token0']: {
                            'idx': 0,
                            'stake_amount': stake_amount * info.get('token0_amount',
                                                                    0) / total_supply if total_supply else 0
                        },
                        info['token1']: {
                            'idx': 1,
                            'stake_amount': stake_amount * info.get('token1_amount',
                                                                    0) / total_supply if total_supply else 0
                        }
                    }
                }

        return result
