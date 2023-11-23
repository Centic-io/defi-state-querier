import logging
from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.databases.mongodb_klg import MongoDB as KLG
logger = logging.getLogger("Lending Pool State Service")
mongo_klg = KLG("")


class PancakeswapServices:
    def __init__(self, state_service: StateQuerier, master_chef_abi, master_chef_contract):

        self.state_service = state_service
        self.chain_id = None
        self.pool_info = {}
        self.token_price = {}
        self.token_decimal = {}
        self.master_chef_abi= master_chef_abi
        self.master_chef_contract= master_chef_contract


    def get_lp_token_function_info(self, lp_token_list, block_number: int = "latest"):
        rpc_calls = {}
        for pid, lp_token in enumerate(lp_token_list):
            for fn_name in ["decimals", "totalSupply", "token0", "token1", "name"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}".lower()

                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

            query_id = f'balanceOf_{lp_token}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf", fn_paras=[self.master_chef_contract],
                block_number=block_number)

            query_id = f'poolInfo_{lp_token}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.master_chef_contract, abi=self.master_chef_abi, fn_name="poolInfo", fn_paras=[pid],
                block_number=block_number)
        return rpc_calls


    def get_balance_of_token_function_info(self, list_farms_info, block_number: int = "latest"):
        rpc_calls = {}
        for lp_token_info, value in list_farms_info.items():
            query_params = lp_token_info.split("_")
            if query_params[0] == "token0" or query_params[0] == "token1":
                lp_token = query_params[1]
                query_id = f'balanceOf_{query_params[0]}_{lp_token}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=value, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[lp_token],
                    block_number=block_number)
        return rpc_calls

    def get_lp_token_price_info(self, lp_token, list_lp_token_balance_info, list_farms_info,
            block_number: int = "latest"):

        total_supply = list_farms_info.get(f'totalsupply_{lp_token}_{block_number}'.lower(), 0)
        token0 = list_farms_info.get(f'token0_{lp_token}_{block_number}'.lower(), "")
        token1 = list_farms_info.get(f'token1_{lp_token}_{block_number}'.lower(), "")

        balance_of_token0 = list_lp_token_balance_info.get(f'balanceOf_token0_{lp_token}_{block_number}'.lower(), 0)
        balance_of_token1 = list_lp_token_balance_info.get(f'balanceOf_token1_{lp_token}_{block_number}'.lower(), 0)
        lp_token_stake_amount = list_farms_info.get(f'balanceOf_{lp_token}_{block_number}'.lower(),
                                                    0)
        if token0 != "" and token1 != "":
            token0_price, token0_decimal = self.get_token_info(token0)
            token1_price, token1_decimal = self.get_token_info(token1)
            if token0_price!=0 and token1_price!=0:
                total_of_token0 = balance_of_token0 / (10 ** token0_decimal) * token0_price
                total_of_token1 = balance_of_token1 / (10 ** token1_decimal) * token1_price
            elif token0_price==0:
                total_of_token1 = balance_of_token1 / (10 ** token1_decimal) * token1_price
                total_of_token0= total_of_token1
                token0_price= total_of_token0/ (balance_of_token0 / (10 ** token0_decimal))
            else:
                total_of_token0 = balance_of_token0/ (10 ** token0_decimal) * token0_price
                total_of_token1 = total_of_token0
                token1_price= total_of_token1/ (balance_of_token1 / (10 ** token1_decimal))
            lp_token_price = (total_of_token0 + total_of_token1) / total_supply
            query_id = f'price_{lp_token}_{block_number}'.lower()
            list_farms_info.update({query_id: lp_token_price})
            token1_stake_amount = lp_token_stake_amount * lp_token_price /2 / token1_price

            token0_stake_amount = lp_token_stake_amount * lp_token_price / 2 / token0_price
            list_farms_info.update({f'amount0_{lp_token}_{block_number}': token0_stake_amount})
            list_farms_info.update({f'amount1_{lp_token}_{block_number}': token1_stake_amount})


    def get_token_info(self, token_address):
        if token_address not in self.token_price:
            token_data = mongo_klg.get_smart_contract("0x38", token_address)
            price = token_data.get("price", 0)
            decimal = token_data.get("decimals", 18)
            self.token_price[token_address] = price
            self.token_decimal[token_address] = decimal

        return self.token_price[token_address], self.token_decimal[token_address]

    ### USER
    def get_user_info_function(self, user: str, lp_token_list: list, block_number: int = "latest"):
        rpc_calls = {}
        for pid, lp_token in enumerate(lp_token_list):
            # lượng token đang hold trong ví

            query_id = f'balanceOf_{user}_{pid}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf",
                fn_paras=[user],
                block_number=block_number)
            # lượng token ví đang stake
            for fn_name in ["userInfo", "pendingCake"]:
                query_id = f'{fn_name}_{user}_{pid}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=self.master_chef_contract, abi=self.master_chef_abi, fn_name=fn_name,
                    fn_paras=[pid, user],
                    block_number=block_number)
        return rpc_calls


    def cal_token_amount_lp_token(self, lp_token, lp_token_amount, list_farms_info, block_number: int = "latest"):
        decimal = list_farms_info.get(f'decimals_{lp_token}_{block_number}'.lower(), 0)
        token0 = list_farms_info.get(f'token0_{lp_token}_{block_number}'.lower(), "")
        token1 = list_farms_info.get(f'token1_{lp_token}_{block_number}'.lower(), "")
        lp_token_price = list_farms_info.get( f'price_{lp_token}_{block_number}'.lower(), 0)
        if token0 != "" and token1 != "":

            token0_price, _ = self.get_token_info(token0)
            token1_price, _ = self.get_token_info(token1)
            token0_amount = lp_token_amount / 10 ** decimal * lp_token_price / 2 / token0_price
            token1_amount = lp_token_amount / 10 ** decimal * lp_token_price / 2 / token1_price
            return token0_amount, token1_amount
        else:
            print(f"lp_token {lp_token} error")
            return 0, 0
