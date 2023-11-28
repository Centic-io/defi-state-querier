import json
import logging
import time

from web3 import Web3

from src.defi_services.jobs.queriers.state_querier import StateQuerier
from src.defi_services.utils.init_dex_services import init_dex_services

logger = logging.getLogger("StateProcessor")


class DexStateProcessor:
    def __init__(self, mongo_klg,  chain_id, provider_uri):
        self.entity_service = None
        self.chain_id= chain_id
        self.provider_url= provider_uri
        self.state_querier = StateQuerier(provider_uri)
        self.services = init_dex_services(self.state_querier,provider_uri,mongo_klg, self.chain_id)


    @staticmethod
    def check_address(address):
        return Web3.isAddress(address)

    @staticmethod
    def checksum_address(address):
        return Web3.toChecksumAddress(address)

    # def init_rpc_call_information(self, wallet, query_id, entity_id, query_type, block_number):

    def run(self, queries:list,wallet, batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False, block_number: int = 'latest',):
        for query in queries:
            query_type= query.get('query_type')
            query_id= query.get('query_id')
            entity_id= query.get('entity_id')
            version= query.get('version', None)
            lp_tokens= query.get("lp_tokens", [])
            if entity_id in self.services:
                self.entity_service = self.services.get(entity_id)
                self.entity_service.get_version(version)
                if query_type=='lptokeninfo':
                    rpc_calls= self.entity_service.get_all_lptoken()
                    result= self.state_querier.query_state_data(rpc_calls, batch_size=batch_size, workers=max_workers,
                                                                      ignore_error=ignore_error)
                    lp_token_list= self.entity_service.return_lp_token(result)
                    list_farms_info= {}
                    # self.init_rpc_call_information(wallet, query_id, entity_id, query_type, block_number)
                    self.run_lp_token(lp_token_list, list_farms_info, batch_size, max_workers, ignore_error)
                    reverse_lp_token_list= {}
                    for key, value in lp_token_list.items():
                        reverse_lp_token_list[value.lower()]= key

                    data= {'lp_token_list': reverse_lp_token_list,
                            'lp_token_info': list_farms_info}
                    with open(f'{entity_id}_{version}_{self.chain_id}_farms_info.json', "w") as f:
                        json.dump(data, f)
                if query_type== 'userinfo' and len(lp_tokens)!=0:

                    with open(f'{entity_id}_{version}_{self.chain_id}_farms_info.json', "r") as f:
                        data= json.loads(f.read())

                    user_info= self.run_user_info_with_specific_lp(wallet, lp_tokens, data, batch_size, max_workers, ignore_error)

                    with open(f'{entity_id}_{version}_{self.chain_id}_user_info.json', "w") as f:
                        json.dump(user_info, f)
    def run_lp_token(self,lp_token_list, list_farms_info,batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False,):
        begin = time.time()
        rpc_calls = self.entity_service.get_lp_token_function_info(lp_token_list)
        list_farms_info.update(
            self.state_querier.query_state_data(rpc_calls, batch_size=batch_size, workers=max_workers,
                                                ignore_error=ignore_error))

        rpc_calls = self.entity_service.get_balance_of_token_function_info(list_farms_info)
        list_farms_info.update(self.state_querier.query_state_data(rpc_calls, batch_size=batch_size,
                                                                   workers=max_workers,
                                                                   ignore_error=ignore_error))

        self.entity_service.update_lp_token_balance_value(list_farms_info)
        self.entity_service.get_lp_token_price_info(lp_token_list, list_farms_info)
        logger.info(f"Get token info list related in {time.time() - begin}s")


    def run_user_info(self, user,  lp_token_list, list_farms_info, batch_size,max_workers, ignore_error ):
        begin = time.time()
        rpc_calls = self.entity_service.get_user_info_function(user, lp_token_list)
        user_info= self.state_querier.query_state_data(rpc_calls, batch_size=batch_size,
                                                                         workers=max_workers, ignore_error=ignore_error)
        self.entity_service.update_stake_token_amount_of_wallet(user, user_info, lp_token_list, list_farms_info)
        logger.info(f"Get token info list related in {time.time() - begin}s")


    def run_user_info_with_specific_lp(self,wallet,  lp_tokens, data,  batch_size: int = 100, max_workers: int = 8, ignore_error: bool = False):
        farms=  data['lp_token_list']
        list_farms_info = data['lp_token_info']
        lp_token_pools=[]
        lp_token_farms= {}
        for lp_token in lp_tokens:
            lp_token= lp_token.lower()
            if lp_token in farms:
                lp_token_farms[lp_token]= farms[lp_token]
            else:
                lp_token_pools.append(lp_token)
        # for
        rpc_calls={}
        for  lp_token,pid in lp_token_farms.items():
            rpc_calls.update(self.entity_service.get_user_info_function(wallet, lp_token, pid, stake= True ))
        for lp_token in lp_token_pools:
            rpc_calls.update(self.entity_service.get_user_info_function(wallet, lp_token, stake= False ))
        user_info= self.state_querier.query_state_data(rpc_calls, batch_size=batch_size,
                                                                         workers=max_workers, ignore_error=ignore_error)
        self.entity_service.update_stake_token_amount_of_wallet(wallet, user_info, list_farms_info)
        return user_info