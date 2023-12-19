import logging
from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.sushiswap_info import (SUSHISWAP_V0_ETH_INFO)
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("SushiSwap V0 Pool State Service")


class SushiSwapInfo:
    mapping = {
        Chain.ethereum: SUSHISWAP_V0_ETH_INFO
    }


class SushiswapServices(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = SushiSwapInfo.mapping.get(chain_id)
        self.masterchef_addr = self.pool_info['masterchef_address']
        self.masterchef_abi = self.pool_info['masterchef_abi']

    def get_all_supported_lp_token(self, limit: int = 1):
        web3 = self.state_service.get_w3()
        if web3.isAddress(self.masterchef_addr):
            self.masterchef_addr = web3.toChecksumAddress(self.masterchef_addr)
        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.poolLength().call()
        rpc_calls = {}
        for pid in range(0, int(pool_length/ limit)):
            query_id = f'poolInfo_{pid}_'
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=[pid]
            )

        return rpc_calls

    def get_service_info(self):
        info = {
            Dex.pancake: {
                "chain_id": self.chain_id,
                "type": "dex",
                "pool_info": self.pool_info
            }
        }
        return info

    def decode_all_supported_lp_token(self, response_data):
        result = {}
        for key, value in response_data.items():
            pid = key.split("_")[1]
            result[value[0]] = {
                "pid": pid}

        return result

    # Get lp token info
    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, pid in lp_token_info.items():
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

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        result = {}
        for lp_token, pid in lp_token_info.items():
            token0 = response_data.get(f'token0_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
            token1 = response_data.get(f'token1_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
            decimals = response_data.get(f'decimals_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
            name = response_data.get(f'name_{lp_token}_{block_number}_{self.chain_id}'.lower(), "")
            total_supply = response_data.get(f'totalsupply_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                             0) / 10 ** decimals
            masterchef_balance = response_data.get(
                f'balanceOf_{lp_token}_{block_number}_{self.chain_id}'.lower()) / 10 ** decimals
            acc_cake_per_share = response_data.get(f'poolInfo_{lp_token}_{block_number}_{self.chain_id}'.lower())[0]
            result[lp_token] = {
                "pid": pid,
                "totalSupply": total_supply,
                "token0": token0,
                "token1": token1,
                "decimals": decimals,
                "name": name,
                "stakeBalance": masterchef_balance,
                "poolInfo": acc_cake_per_share
            }
        return result

    # Get balance of token
    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for key, value in lp_token_info.items():
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[key],
                        block_number=block_number)

                    rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(
            self, supplied_data, balance_info, block_number: int = "latest"):
        lp_token_balance = {}
        lp_token_info = supplied_data['lp_token_info']
        token_info = supplied_data['token_info']
        for key, value in lp_token_info.items():
            lp_token_balance[key] = {}
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    lp_token_balance[key][token] = balance_info.get(query_id) / 10 ** balance_info.get(
                        decimals_query_id)
        result = self.calculate_lp_token_price_info(lp_token_info, lp_token_balance, token_info)
        return result

    # Calculate lp token price
    def calculate_lp_token_price_info(
            self, lp_token_info, lp_token_balance, token_price):
        result = {}
        for lp_token, value in lp_token_info.items():
            total_supply = value.get("totalSupply")
            token0 = value.get("token0", None)
            token1 = value.get("token1", None)
            if token0 and token1:
                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                lp_token_stake_amount = value.get("stakeBalance", 0)
                result[lp_token] = {
                    "totalSupply": total_supply,
                    "stakeBalance": lp_token_stake_amount,
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1
                }
                if token0 and token1:
                    token0_price = token_price.get(token0).get("price", 0)
                    token1_price = token_price.get(token1).get("price", 0)
                    new_amount1 = balance_of_token1
                    if token0_price != 0 and token1_price != 0:
                        total_of_token0 = balance_of_token0 * token0_price
                        total_of_token1 = balance_of_token1 * token1_price
                    elif token0_price == 0:
                        total_of_token1 = balance_of_token0 * token1_price
                        total_of_token0 = total_of_token1
                        token0_price = total_of_token0 / balance_of_token0
                    else:
                        total_of_token0 = balance_of_token1 * token0_price
                        total_of_token1 = total_of_token0
                        token1_price = total_of_token1 / new_amount1
                    lp_token_price = (total_of_token0 + total_of_token1) / total_supply
                    result[lp_token].update({
                        "price": lp_token_price,
                        'token0Price': token0_price,
                        'token1Price': token1_price,
                        "stakeAmountToken0": lp_token_stake_amount * lp_token_price / 2 / token0_price,
                        "stakeAmountToken1": lp_token_stake_amount * lp_token_price / 2 / token1_price
                    })

        return result

    # USER ##
    def get_user_info_function(
            self, user: str, supplied_data, stake: bool = True, block_number: int = "latest"):
        rpc_calls = {}
        # lượng token đang hold trong ví
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            query_id = f'balanceOf_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf",
                fn_paras=[user],
                block_number=block_number)
            decimals_query_id = f'decimals_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="decimals", block_number=block_number)

            # lượng token ví đang stake
            if stake:
                query_id = f'userInfo_{user}_{lp_token}_{pid}_{block_number}'.lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="userInfo",
                    fn_paras=[int(pid), user],
                    block_number=block_number)

        return rpc_calls

    def decode_user_info_function(
            self, user: str, supplied_data: dict, user_data: dict, token_price: dict = None, stake: bool = True,
            block_number: int = "latest"):
        user_info = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            query_id = f'balanceOf_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower()
            decimals = user_data.get(f'decimals_{user}_{lp_token}_{block_number}_{self.chain_id}'.lower())
            user_info[lp_token] = {
                "amount": user_data.get(query_id) / 10 ** decimals,
                "decimals": decimals
            }
            # lượng token ví đang stake
            if stake:
                query_id = f'userInfo_{user}_{lp_token}_{pid}_{block_number}'.lower()
                user_info[lp_token]["userInfo"] = user_data.get(query_id)

        result = self.update_stake_token_amount_of_wallet(user_info, lp_token_info)
        return result

    def update_stake_token_amount_of_wallet(
            self, user_info, lp_token_info: dict = None):
        user_info_token_amount = {}
        for lp_token, value in user_info.items():
            pair_info = lp_token_info.get(lp_token)
            amount = value.get("amount", 0)
            user_info_token_amount[lp_token] = {
                "amount": amount
            }
            if value.get("userInfo") and pair_info:
                pid = pair_info.get("pid")
                if not pid:
                    continue
                decimals = value.get("decimals")
                stake_amount = value.get("userInfo", [0])[0] / 10 ** decimals
                if stake_amount > 0:
                    user_info_token_amount[lp_token]["stakeAmount"] = stake_amount
                    token_pair_amount = self.cal_token_amount_lp_token(
                        amount, stake_amount, pair_info)
                    user_info_token_amount[lp_token].update(token_pair_amount)

        return user_info_token_amount

    def cal_token_amount_lp_token(self, lp_token_amount, stake_lp_amount, list_token_info):
        token0, token1 = list_token_info.get("token0"), list_token_info.get("token1")
        result = {}
        if token0 and token1:
            token0_price, token1_price = list_token_info.get('token0Price'), list_token_info.get('token1Price')
            lp_token_price = list_token_info.get("price")
            lp_token_amount_in_usd = lp_token_amount * lp_token_price
            stake_lp_amount_in_usd = stake_lp_amount * lp_token_price
            token0_amount = lp_token_amount_in_usd / 2 / token0_price
            token1_amount = lp_token_amount_in_usd / 2 / token1_price
            result = {
                "valueInUSD": lp_token_amount_in_usd,
                "stakeValueInUSD": stake_lp_amount_in_usd,
                token0: {
                    "amount": token0_amount,
                    "stakeAmount": stake_lp_amount_in_usd / 2 / token0_price,
                    "valueInUSD": lp_token_amount_in_usd / 2,
                    "stakeValueInUSD": stake_lp_amount_in_usd / 2,
                },
                token1: {
                    "amount": token1_amount,
                    "stakeAmount": stake_lp_amount_in_usd / 2 / token1_price,
                    "valueInUSD": lp_token_amount_in_usd / 2,
                    "stakeValueInUSD": stake_lp_amount_in_usd / 2,
                }
            }

        return result

    # Reward
    def get_rewards_balance_function_info(self, user, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data.get("lp_token_info")
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            query_id = f'pendingSushi_{user}_{lp_token}_{pid}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="pendingSushi",
                fn_paras=[int(pid), user], block_number=block_number)
        return rpc_calls

    def calculate_rewards_balance(
            self,
            user: str,
            lp_token_info: dict,
            decoded_data: dict,
            block_number: int = "latest"
    ) -> dict:
        amount = 0
        for lp_token, value in lp_token_info.items():
            pid = value.get("pid")
            query_id = f'pendingSushi_{user}_{lp_token}_{pid}_{block_number}'.lower()
            amount += decoded_data.get(query_id) / 10 ** 18
        result = {self.pool_info.get("rewardToken"): amount}
        return result
