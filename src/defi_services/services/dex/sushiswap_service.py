from web3 import Web3

from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from src.defi_services.constants.chain_constant import Chain

from src.defi_services.jobs.queriers.state_querier import StateQuerier
from src.defi_services.databases.mongodb_klg import MongoDB as KLG
from src.defi_services.services.dex.dex_info.sushiswap_info import *
from src.defi_services.services.dex.dex_protocol_services import DexProtocolServices


# logger = logging.getLogger("Lending Pool State Service")

class SushiSwapInfo:
    mapping = {
        Chain.bsc: [SUSHISWAP_BSC_INFO],
        Chain.fantom: [SUSHISWAP_FANTOM_INFO],
        Chain.polygon: [SUSHISWAP_POLYGON_INFO],
        Chain.optimism: [SUSHISWAP_OPTIMISM_INFO],
        Chain.avalanche: [SUSHISWAP_AVALANCHE_INFO],
        Chain.arbitrum: [SUSHISWAP_ARBITRUM_INFO],
        Chain.ethereum: [SUSHISWAP_V0_ETH_INFO, SUSHISWAP_V2_ETH_INFO]
        }


class SushiswapServices(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, provider, mongo_klg: KLG() = None, chain_id: str = '0x38'):
        super().__init__(mongo_klg)
        self.chain_id = chain_id
        self.state_service = state_service
        self.mongo_klg = mongo_klg
        self.token_price = {}
        self.provider = provider
        self.token_decimal = {}

    def get_all_lptoken(self, version: int = None):
        if self.chain_id == '0x1' and version == 2:
            self.masterchef_addr = SushiSwapInfo.mapping.get(self.chain_id)[1]['masterchef_address']
            self.masterchef_abi = SushiSwapInfo.mapping.get(self.chain_id)[1]['masterchef_abi']

        else:
            self.masterchef_addr = SushiSwapInfo.mapping.get(self.chain_id)[0]['masterchef_address']
            self.masterchef_abi = SushiSwapInfo.mapping.get(self.chain_id)[0]['masterchef_abi']

        web3 = Web3(Web3.HTTPProvider(self.provider))
        if web3.isAddress(self.masterchef_addr):
            self.masterchef_addr = web3.toChecksumAddress(self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.poolLength().call()
        rpc_calls = {}

        if version == 0 and self.chain_id == '0x1':
            for pid in range(0, pool_length):
                query_id = f'poolInfo_{pid}_'
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[pid]
                    )
        else:
            for pid in range(0, pool_length):
                query_id = f'lpToken_{pid}_'
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="lpToken", fn_paras=[pid]
                    )
        return rpc_calls

    def get_lp_token_function_info(self, lp_token_list, block_number: int = "latest"):
        rpc_calls = {}
        for pid, lp_token in lp_token_list.items():
            for fn_name in ["decimals", "totalSupply", "token0", "token1", "name"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}_{self.chain_id}".lower()

                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=LP_TOKEN_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

            query_id = f'balanceOf_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf", fn_paras=[self.masterchef_addr],
                block_number=block_number)

            query_id = f'poolInfo_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[int(pid)],
                block_number=block_number)
        return rpc_calls

    def get_balance_of_token_function_info(self, list_farms_info, block_number: int = "latest"):
        rpc_calls = {}
        for lp_token_info, value in list_farms_info.items():
            query_params = lp_token_info.split("_")
            fn_name = query_params[0]
            if fn_name == "token0" or fn_name == "token1":
                lp_token = query_params[1]
                query_id = f'amount{fn_name[-1]}_{lp_token}_{block_number}_{self.chain_id}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=value, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[lp_token],
                    block_number=block_number)
        return rpc_calls

    def get_lp_token_price_info(self, lp_token_list, list_farms_info,
            block_number: int = "latest"):
        for pid, lp_token in lp_token_list.items():
            total_supply = list_farms_info.get(f'totalsupply_{lp_token}_{block_number}_{self.chain_id}'.lower(), 0)
            token0 = list_farms_info.get(f'token0_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
            token1 = list_farms_info.get(f'token1_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")

            balance_of_token0 = list_farms_info.get(f'amount0_{lp_token}_{block_number}_{self.chain_id}'.lower(), 0)
            balance_of_token1 = list_farms_info.get(f'amount1_{lp_token}_{block_number}_{self.chain_id}'.lower(), 0)
            lp_token_stake_amount = list_farms_info.get(f'balanceOf_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                                        0)
            if token0 != "" and token1 != "":
                token0_price, token0_decimal = self.get_token_info(token0)
                new_amount0 = balance_of_token0 / (10 ** token0_decimal)
                token1_price, token1_decimal = self.get_token_info(token1)
                new_amount1 = balance_of_token1 / (10 ** token1_decimal)
                list_farms_info.update({f'amount0_{lp_token}_{block_number}_{self.chain_id}'.lower(): new_amount0})
                list_farms_info.update({f'amount1_{lp_token}_{block_number}_{self.chain_id}'.lower(): new_amount1})
                if token0_price != 0 and token1_price != 0:
                    total_of_token0 = new_amount0 * token0_price
                    total_of_token1 = new_amount1 * token1_price
                elif token0_price == 0:
                    total_of_token1 = new_amount1 * token1_price
                    total_of_token0 = total_of_token1
                    token0_price = total_of_token0 / new_amount0
                else:
                    total_of_token0 = new_amount0 * token0_price
                    total_of_token1 = total_of_token0
                    token1_price = total_of_token1 / new_amount1
                lp_token_price = (total_of_token0 + total_of_token1) / total_supply
                query_id = f'price_{lp_token}_{block_number}_{self.chain_id}'.lower()
                list_farms_info.update({query_id: lp_token_price})
                list_farms_info.update({f'price0_{lp_token}_{block_number}_{self.chain_id}'.lower(): token0_price})
                list_farms_info.update({f'price1_{lp_token}_{block_number}_{self.chain_id}'.lower(): token1_price})
                token1_stake_amount = lp_token_stake_amount * lp_token_price / 2 / token1_price
                token0_stake_amount = lp_token_stake_amount * lp_token_price / 2 / token0_price
                list_farms_info.update(
                    {f'stakeamount0_{lp_token}_{block_number}_{self.chain_id}'.lower(): token0_stake_amount})
                list_farms_info.update(
                    {f'stakeamount1_{lp_token}_{block_number}_{self.chain_id}'.lower(): token1_stake_amount})

    def get_token_info(self, token_address):
        if token_address not in self.token_price:
            token_data = self.mongo_klg.get_smart_contract(self.chain_id, token_address)
            price = token_data.get("price", 0)
            decimal = token_data.get("decimals", 18)
            self.token_price[token_address] = price
            self.token_decimal[token_address] = decimal

        return self.token_price[token_address], self.token_decimal[token_address]

    def update_lp_token_balance_value(self, list_farms_info):
        for rpc_call_id, value in list_farms_info.items():
            fn_name = rpc_call_id.split("_")[0]
            lp_token = rpc_call_id.split("_")[1]

            if fn_name == "balanceof":
                decimal = list_farms_info.get(f'decimals_{lp_token}_latest', 18)
                list_farms_info[rpc_call_id] = value / 10 ** decimal
            if fn_name == "totalsupply":
                decimal = list_farms_info.get(f'decimals_{lp_token}_latest', 18)
                list_farms_info[rpc_call_id] = value / 10 ** decimal

    ### USER
    def get_user_info_function(self, user: str, lp_token_list: list, block_number: int = "latest"):
        rpc_calls = {}
        for pid, lp_token in enumerate(lp_token_list):
            # lượng token đang hold trong ví

            query_id = f'balanceOf_{user}_{pid}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf",
                fn_paras=[user],
                block_number=block_number)
            # lượng token ví đang stake
            # if self.masterchef_abi == PANCAKESWAP_MASTER_CHEF_V2_CONTRACT:
            #     for fn_name in ["userInfo", "pendingCake"]:
            #         query_id = f'{fn_name}_{user}_{pid}_{block_number}'.lower()
            #         rpc_calls[query_id] = self.state_service.get_function_info(
            #             address=self.dex_info['masterchef_address'], abi=self.masterchef_abi, fn_name=fn_name,
            #             fn_paras=[pid, user],
            #             block_number=block_number)
            # elif self.masterchef_abi == SUSHI_SWAP_MASTERCHEF_V2_CONTRACT:
            #     for fn_name in ["userInfo", "pendingSushi"]:
            #         query_id = f'{fn_name}_{user}_{pid}_{block_number}'.lower()
            #         rpc_calls[query_id] = self.state_service.get_function_info(
            #             address=self.dex_info['masterchef_address'], abi=self.masterchef_abi, fn_name=fn_name,
            #             fn_paras=[pid, user],
            #             block_number=block_number)
        return rpc_calls

    def cal_token_amount_lp_token(self, lp_token, lp_token_amount, list_farms_info, block_number: int = "latest"):
        decimal = list_farms_info.get(f'decimals_{lp_token}_{block_number}_{self.chain_id}'.lower(), 0)
        token0 = list_farms_info.get(f'token0_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
        token1 = list_farms_info.get(f'token1_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
        lp_token_price = list_farms_info.get(f'price_{lp_token}_{block_number}_{self.chain_id}'.lower(), 0)
        if token0 != "" and token1 != "":

            token0_price, _ = self.get_token_info(token0)
            token1_price, _ = self.get_token_info(token1)
            token0_amount = lp_token_amount * lp_token_price / 2 / token0_price
            token1_amount = lp_token_amount * lp_token_price / 2 / token1_price
            return token0_amount, token1_amount
        else:
            print(f"lp_token {lp_token} error")
            return 0, 0

    def update_stake_token_amount_of_wallet(self, user, user_info, lp_token_list, list_farms_info):

        user_info_token_amount = {}
        for query_id, amount in user_info.items():
            query_id_split = query_id.split("_")
            pid = int(query_id_split[2])
            lp_token = lp_token_list[pid]
            if query_id_split[0] == "balanceof":
                if amount > 0:
                    decimal = list_farms_info[f'decimals_{lp_token}_latest_{self.chain_id}'.lower()]
                    amount = amount / 10 ** decimal
                    user_info.update({query_id: amount})
                    token0_amount, token1_amount = self.cal_token_amount_lp_token(lp_token, amount, list_farms_info)
                    user_info_token_amount.update({f'hold0_{user}_{pid}_{self.chain_id}'.lower(): token0_amount})
                    user_info_token_amount.update({f'hold1_{user}_{pid}_{self.chain_id}'.lower(): token1_amount})
                    query_id = f'totallp_{user}_{pid}'.lower()
                    if query_id not in user_info_token_amount:
                        user_info_token_amount[query_id] = amount
                        user_info_token_amount[f'total0_{user}_{pid}_{self.chain_id}'.lower()] = token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}_{self.chain_id}'.lower()] = token1_amount
                    else:
                        user_info_token_amount[query_id] += amount
                        user_info_token_amount[f'total0_{user}_{pid}_{self.chain_id}'.lower()] += token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}_{self.chain_id}'.lower()] += token1_amount

            elif query_id_split[0] == 'userinfo':
                if amount[0] > 0:
                    token0_amount, token1_amount = self.cal_token_amount_lp_token(lp_token, amount[0], list_farms_info)
                    user_info_token_amount.update({f'stake0_{user}_{pid}_{self.chain_id}'.lower(): token0_amount})
                    user_info_token_amount.update({f'stake1_{user}_{pid}_{self.chain_id}'.lower(): token1_amount})
                    query_id = f'totallp_{user}_{pid}_{self.chain_id}'.lower()
                    if query_id not in user_info_token_amount:
                        user_info_token_amount[query_id] = amount
                        user_info_token_amount[f'total0_{user}_{pid}_{self.chain_id}'.lower()] = token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}_{self.chain_id}'.lower()] = token1_amount
                    else:
                        user_info_token_amount[query_id] += amount
                        user_info_token_amount[f'total0_{user}_{pid}_{self.chain_id}'.lower()] += token0_amount
                        user_info_token_amount[f'total1_{user}_{pid}_{self.chain_id}'.lower()] += token1_amount
        user_info.update(user_info_token_amount)

