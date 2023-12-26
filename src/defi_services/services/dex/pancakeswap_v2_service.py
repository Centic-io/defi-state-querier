import logging

from defi_services.abis.dex.pancakeswap.pancakeswap_factory_abi import PANCAKESWAP_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_masterchef_v2_abi import PANCAKESWAP_MASTERCHEF_V2_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.pancakeswap_info import PANCAKESWAP_V2_BSC_INFO
from defi_services.services.dex.uniswap_v2_service import UniswapV2Services

logger = logging.getLogger("PancakeSwap V2 State Service")


class PancakeSwapV2Info:
    mapping = {
        Chain.bsc: PANCAKESWAP_V2_BSC_INFO
    }


class PancakeSwapV2Services(UniswapV2Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__(state_service=state_service, chain_id=chain_id)

        self.pool_info = PancakeSwapV2Info.mapping.get(chain_id)
        self.masterchef_abi = PANCAKESWAP_MASTERCHEF_V2_ABI
        self.factory_abi = PANCAKESWAP_FACTORY_ABI

    def get_service_info(self):
        info = {
            Dex.pancake_v2: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    # Get all lp tokens
    def get_farming_supported_lp_token(self, limit: int = 1):
        web3 = self.state_service.get_w3()
        masterchef_addr = self.pool_info.get('masterchefAddress')

        master_chef_contract = web3.eth.contract(abi=self.masterchef_abi, address=web3.toChecksumAddress(masterchef_addr))
        pool_length = master_chef_contract.functions.poolLength().call()

        rpc_calls = {}
        for pid in range(0, min(pool_length, limit)):
            query_id = f'lpToken_{masterchef_addr}_{pid}_latest'.lower()
            rpc_calls[query_id] = self.get_masterchef_function_info(fn_name="lpToken", fn_paras=[pid])

        # For another version
        # masterchef_addr_v1 = self.pool_info.get('masterchefAddressV1')
        # master_chef_contract_v1 = web3.eth.contract(abi=self.masterchef_v1_abi, address=web3.toChecksumAddress(masterchef_addr_v1))
        # pool_length_v1 = master_chef_contract_v1.functions.poolLength().call()
        #
        # for pid in range(0, min(pool_length_v1, limit)):
        #     query_id = f'poolInfo_{masterchef_addr}_{pid}_latest'.lower()
        #     rpc_calls[query_id] = self.get_masterchef_v1_function_info(fn_name="poolInfo", fn_paras=[pid])

        return rpc_calls

    def decode_farming_supported_lp_token(self, decoded_data):
        result = {}
        for query_id, value in decoded_data.items():
            # Format query_id: f'lpToken_{self.masterchef_addr}_{pid}_latest'

            pid = int(query_id.split("_")[-2])
            result[value.lower()] = {"farming_pid": pid}

            # For another version
            # elif query_id.startswith('poolInfo'):
            #     lp_token = value[0].lower()
            #     if lp_token not in result:
            #         result[lp_token] = {}
            #
            #     # Format query_id: f'poolInfo_{self.masterchef_addr}_{pid}_latest'
            #     pid = int(query_id.split("_")[-2])
            #     result[lp_token] = {"farming_v1_pid": pid}

        return result

    # Get lp token info
    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = super().get_lp_token_function_info(supplied_data=supplied_data, block_number=block_number)

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf", fn_paras=[masterchef_addr],
                block_number=block_number)

            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                query_id = f'poolInfo_{masterchef_addr}_{pid}_{block_number}'.lower()
                rpc_calls[query_id] = self.get_masterchef_function_info(
                    fn_name="poolInfo", fn_paras=[pid], block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, decoded_data, block_number: int = "latest"):
        result = super().decode_lp_token_info(
            supplied_data=supplied_data, decoded_data=decoded_data, block_number=block_number)

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            lp_info = result.get(lp_token, {})

            staked_balance_query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()

            if (not lp_info) or (decoded_data.get(staked_balance_query_id) is None):
                continue

            masterchef_balance = decoded_data.get(
                staked_balance_query_id) / 10 ** lp_info.get('decimals', 18)
            lp_info.update({"stake_balance": masterchef_balance})

            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                pool_info_query_id = f'poolInfo_{masterchef_addr}_{pid}_{block_number}'.lower()
                pool_info = decoded_data.get(pool_info_query_id)
                acc_cake_per_share = pool_info[0] / 10 ** 18
                alloc_point = pool_info[2]

                lp_info.update({
                    'acc_reward_per_share': acc_cake_per_share,
                    'alloc_point': alloc_point,
                    'farming_pid': pid
                })

        return result

    # Get balance of token
    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = super().get_balance_of_token_function_info(
            supplied_data=supplied_data, block_number=block_number
        )

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=lp_token, abi=LP_TOKEN_ABI, fn_name="balanceOf", fn_paras=[masterchef_addr],
                block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(self, supplied_data, decoded_data, block_number: int = "latest"):
        result = super().decode_balance_of_token_function_info(
            supplied_data=supplied_data, decoded_data=decoded_data, block_number=block_number
        )

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            lp_info = result.get(lp_token, {})

            staked_balance_query_id = f'balanceOf_{lp_token}_{masterchef_addr}_{block_number}'.lower()

            if (not lp_info) or (decoded_data.get(staked_balance_query_id) is None):
                continue

            staked_balance = decoded_data.get(
                staked_balance_query_id) / 10 ** lp_info.get('decimals', 18)
            lp_info.update({"stake_balance": staked_balance})

            for token_key in ["token0", "token1"]:
                token_amount = lp_info.get(f'{token_key}_amount', 0)
                token_stake_amount = token_amount * staked_balance / lp_info.get('total_supply') if lp_info.get('total_supply') else 0
                result[lp_token][f'{token_key}_stake_amount'] = token_stake_amount

        return result

    # Calculate lp token price
    def calculate_lp_token_price_info(
            self, supplied_data, lp_token_balance, token_price):
        """Deprecated"""
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            total_supply = value.get("totalSupply")
            token0 = value.get("token0", None)
            token1 = value.get("token1", None)
            if token0 and token1:

                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                lp_token_stake_amount = value.get("stakeBalance", 0)
                lp_token_info[lp_token].update({
                    "totalSupply": total_supply,
                    "stakeBalance": lp_token_stake_amount,
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1
                })
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
                lp_token_info[lp_token].update({
                    "price": lp_token_price,
                    'token0Price': token0_price,
                    'token1Price': token1_price,
                    "stakeAmountToken0": lp_token_stake_amount * lp_token_price / 2 / token0_price,
                    "stakeAmountToken1": lp_token_stake_amount * lp_token_price / 2 / token1_price
                })

        return lp_token_info

    # User Information
    def get_user_info_function(
            self, wallet: str, supplied_data, stake: bool = True, block_number: int = "latest"):
        rpc_calls = super().get_user_info_function(
            wallet=wallet, supplied_data=supplied_data, stake=stake, block_number=block_number)

        masterchef_addr = self.pool_info.get('masterchefAddress')

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

        result = super().decode_user_info_function(
            wallet=wallet, supplied_data=supplied_data, decoded_data=decoded_data,
            stake=stake, block_number=block_number
        )

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if stake and (info.get('farming_pid') is not None):
                pid = int(info.get('farming_pid'))
                query_id = f'userInfo_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                user_info = decoded_data.get(query_id)
                stake_amount = user_info[0] / 10 ** info.get('decimals', 18) if user_info else 0

                total_supply = info.get('total_supply')

                result[lp_token]['farming_pid'] = pid
                result[lp_token]['stake_amount'] = stake_amount
                result[lp_token]['tokens'][info['token0']]['stake_amount'] = stake_amount * info.get('token0_amount', 0) / total_supply if total_supply else 0
                result[lp_token]['tokens'][info['token1']]['stake_amount'] = stake_amount * info.get('token1_amount', 0) / total_supply if total_supply else 0

        return result

    def update_stake_token_amount_of_wallet(self, user_info, supplied_data: dict = None):
        """Deprecated"""
        user_info_token_amount = {}
        lp_token_info = supplied_data['lp_token_info']
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
        """Deprecated"""
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

                query_id = f'pendingCake_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()
                rpc_calls[query_id] = self.get_masterchef_function_info(
                    fn_name="pendingCake", fn_paras=[int(pid), wallet], block_number=block_number)

        return rpc_calls

    def calculate_rewards_balance(self, wallet: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest") -> dict:
        reward_token = self.pool_info.get("rewardToken")
        reward_decimals = decoded_data.get(f'decimals_{reward_token}_{block_number}'.lower())

        result = {}

        masterchef_addr = self.pool_info.get('masterchefAddress')

        lp_token_info = supplied_data['lp_token_info']
        for lp_token, info in lp_token_info.items():
            if info.get('farming_pid') is not None:
                pid = int(info.get('farming_pid'))
                query_id = f'pendingCake_{masterchef_addr}_{[pid, wallet]}_{block_number}'.lower()

                result[lp_token] = {reward_token: {'amount': decoded_data.get(query_id) / 10 ** reward_decimals}}

        return result

    def get_masterchef_function_info(self, fn_name, fn_paras, block_number: int = 'latest'):
        masterchef_addr = self.pool_info['masterchefAddress']
        return self.state_service.get_function_info(
            masterchef_addr, self.masterchef_abi, fn_name, fn_paras, block_number
        )
