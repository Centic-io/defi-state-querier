import json
import logging
import time

from web3 import Web3

from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.pancake_swap_v2_service import PancakeswapServices

logger = logging.getLogger("StateProcessor")


class DexStateProcessor:
    def __init__(self, provider_uri, master_chef_abi, master_chef_contract):
        self.provider_url= provider_uri
        self.list_farms_info={}

        self.services = PancakeswapServices(StateQuerier(provider_uri), master_chef_abi, master_chef_contract)
        self.state_querier = StateQuerier(provider_uri)


    @staticmethod
    def check_address(address):
        return Web3.isAddress(address)

    @staticmethod
    def checksum_address(address):
        return Web3.toChecksumAddress(address)

    # def init_rpc_call(self):

    def run(self,lp_token_list,user, batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False):

        self.run_lp_token_info(lp_token_list, batch_size,max_workers, ignore_error)
        self.run_user_info(user,  lp_token_list,batch_size,max_workers, ignore_error )


    def run_lp_token_info(self, lp_token_list, batch_size,max_workers, ignore_error):
        begin = time.time()
        rpc_calls=self.services.get_lp_token_function_info(lp_token_list)
        self.list_farms_info.update(self.state_querier.query_state_data(rpc_calls, batch_size=batch_size, workers=max_workers,
                                                              ignore_error=ignore_error))


        rpc_calls = self.services.get_balance_of_token_function_info(self.list_farms_info)
        list_lp_token_balance_info = self.state_querier.query_state_data(rpc_calls, batch_size=batch_size,
                                                                         workers=max_workers, ignore_error=ignore_error)
        for query_id, value in self.list_farms_info.items():
            fn_name = query_id.split("_")[0]
            lp_token=  query_id.split("_")[1]

            if fn_name == "balanceof":
                decimal = self.list_farms_info.get(f'decimals_{lp_token}_latest', 18)
                self.list_farms_info[query_id]= value/ 10**decimal
            if fn_name=="totalsupply":
                decimal = self.list_farms_info.get(f'decimals_{lp_token}_latest', 18)
                self.list_farms_info[query_id]= value/ 10**decimal

        for lp_token in lp_token_list:
            self.services.get_lp_token_price_info(lp_token, list_lp_token_balance_info, self.list_farms_info)


        with open('list_farm_info.json', "w") as f:
            json.dump(self.list_farms_info, f)

        logger.info(f"Get token info list related in {time.time() - begin}s")


    def run_user_info(self, user,  lp_token_list,batch_size,max_workers, ignore_error ):
        begin = time.time()
        rpc_calls = self.services.get_user_info_function(user, lp_token_list)
        user_info = self.state_querier.query_state_data(rpc_calls, batch_size=batch_size,
                                                                         workers=max_workers, ignore_error=ignore_error)

        user_info_token_amount={}
        for query_id, amount in user_info.items():
            query_id_split = query_id.split("_")
            pid= int(query_id_split[2])
            lp_token= lp_token_list[pid]
            if query_id_split[0]== "balanceof":
                if amount>0:
                    token0_amount, token1_amount= self.services.cal_token_amount_lp_token(lp_token, amount, self.list_farms_info)
                    user_info_token_amount.update({f'hold0_{user}_{pid}'.lower(): token0_amount})
                    user_info_token_amount.update({f'hold1_{user}_{pid}'.lower(): token1_amount})
                    query_id=f'totallp_{user}_{pid}'.lower()
                    if query_id not in user_info_token_amount:
                        user_info_token_amount[query_id]= amount
                        user_info_token_amount[f'total0_{user}_{pid}'.lower()]= token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}'.lower()]= token1_amount
                    else:
                        user_info_token_amount[query_id]+= amount
                        user_info_token_amount[f'total0_{user}_{pid}'.lower()]+= token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}'.lower()]+= token1_amount

            elif query_id_split[0] == 'userinfo':
                if amount[0]>0:
                    token0_amount, token1_amount = self.services.cal_token_amount_lp_token(lp_token, amount[0], self.list_farms_info)
                    user_info_token_amount.update({f'stake0_{user}_{pid}'.lower(): token0_amount})
                    user_info_token_amount.update({f'stake1_{user}_{pid}'.lower(): token1_amount})
                    query_id = f'totallp_{user}_{pid}'.lower()
                    if query_id not in user_info_token_amount:
                        user_info_token_amount[query_id] = amount
                        user_info_token_amount[f'total0_{user}_{pid}'.lower()] = token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}'.lower()] = token1_amount
                    else:
                        user_info_token_amount[query_id] += amount
                        user_info_token_amount[f'total0_{user}_{pid}'.lower()] += token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}'.lower()] += token1_amount
        user_info.update(user_info_token_amount)
        with open('user_info.json', "w") as f:
            json.dump(user_info, f)
        logger.info(f"Get token info list related in {time.time() - begin}s")






