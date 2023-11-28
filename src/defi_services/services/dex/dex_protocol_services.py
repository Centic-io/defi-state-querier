import logging

from src.defi_services.databases.mongodb_klg import MongoDB as KLG

logger = logging.getLogger("Lending Pool State Service")


class DexProtocolServices:
    def __init__(self, mongo_klg: KLG() = None):
        self.mongo_klg = mongo_klg
        self.token_price = {}
        self.chain_id = None
        self.token_decimal = {}

    def return_lp_token(self, raw_lp_token_list):
        query_id , _= next(iter(raw_lp_token_list.items()))
        fn_name_sample= query_id.split("_")[0]
        lp_token_list = {}
        if fn_name_sample == 'lpToken':
            for query_id, lp_token in raw_lp_token_list.items():
                pid = query_id.split("_")[1]
                lp_token_list[pid] = lp_token

        if fn_name_sample == "poolInfo":
            for query_id, lp_token in raw_lp_token_list.items():
                pid = query_id.split("_")[1]
                lp_token_list[pid] = lp_token[0]
        return lp_token_list

    def get_all_lptoken(self):
        ...

    def get_lp_token_function_info(self, lp_token_list, block_number: int = "latest"):
        return {}

    def update_lp_token_balance_value(self, list_farms_info: dict):
        ...

    def get_balance_of_token_function_info(self, list_farms_info, block_number: int = "latest"):
        return {}

    def get_lp_token_price_info(self, lp_token_list, list_farms_info):
        ...

    def update_stake_token_amount_of_wallet(self, user, user_info,  list_farms_info):
        ...

    def get_token_info(self, token_address):
        if token_address not in self.token_price:
            token_data = self.mongo_klg.get_smart_contract(self.chain_id, token_address)
            price = token_data.get("price", 0)
            decimal = token_data.get("decimals", 18)
            self.token_price[token_address] = price
            self.token_decimal[token_address] = decimal

        return self.token_price[token_address], self.token_decimal[token_address]

    ### USER
    def get_user_info_function(self, user: str, lp_token_list: list, block_number: int = "latest"):
        return {}

