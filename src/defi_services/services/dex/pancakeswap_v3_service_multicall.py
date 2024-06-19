import copy
import logging
import math
from typing import List

from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.blockchain.multicall_v2 import W3Multicall
from defi_services.services.dex.dex_info.pancakeswap_info import PANCAKESWAP_V3_BSC_INFO
from defi_services.services.dex.uniswap_v3_service_multicall import UniswapV3Services
from defi_services.utils.get_fees import get_fees
from defi_services.utils.sqrt_price_math import get_token_amount_of_pool, get_token_amount_of_user

logger = logging.getLogger("PancakeSwap V3 State Service")


class PancakeSwapV3Info:
    mapping = {
        Chain.bsc: PANCAKESWAP_V3_BSC_INFO
    }


class PancakeSwapV3Service(UniswapV3Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x38'):
        super().__init__(state_service=state_service, chain_id=chain_id)
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = PancakeSwapV3Info.mapping.get(chain_id)
        self.web3 = self.state_service.get_w3()

        if self.pool_info is not None:
            self.masterchef_addr = self.pool_info['master_chef_address']
            self.masterchef_abi = self.pool_info['master_chef_abi']
            self.factory_addr = self.pool_info['factory_address']
            self.factory_abi = self.pool_info.get('factory_abi')
            self.nft_token_manager_addr = self.pool_info['NFT_manager_address']
            self.nft_token_manager_abi = self.pool_info['NFT_manager_abi']

    def get_service_info(self):
        info = {
            Dex.pancake_v3: {
                "chain_id": self.chain_id,
                "type": "dex",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit: int = 10000, supplied_data: dict = None):
        multicall_calls: List['W3Multicall.Call'] = []
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)

        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 2500, 10000]:
                    multicall_calls.append(W3Multicall.Call(
                        address=self.factory_addr, abi=self.factory_abi, fn_name="getPool",
                        fn_paras=[self.web3.to_checksum_address(token0), self.web3.to_checksum_address(token1), fee]))

        return multicall_calls

    def decode_all_supported_lp_token(self, limit: int = 10000, decoded_data: dict = None, supplied_data: dict = None):
        result = {}
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)
        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 2500, 10000]:
                    query_id = f'getPool_{self.factory_addr}_{[token0, token1, fee]}_latest'.lower()
                    pool_address = decoded_data.get(query_id)
                    if pool_address != '0x0000000000000000000000000000000000000000':
                        result[pool_address] = {
                            'token0': token0,
                            'token1': token1,
                            'fee': fee
                        }

        return result

    def get_farming_supported_lp_token(self, limit: int = 10000, supplied_data: dict = None):
        self.masterchef_addr = self.checksum_address(self.masterchef_addr)
        master_chef_contract = self.web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        pool_length = master_chef_contract.functions.poolLength().call()
        multicall_calls: List['W3Multicall.Call'] = []

        for pid in range(1, min(pool_length, limit)):
            multicall_calls.append(W3Multicall.Call(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo",
                fn_paras=pid, block_number='latest'))

        return multicall_calls

    def decode_farming_supported_lp_token(self, response_data, supplied_data: dict = None):
        result = {}
        for query_id, value in response_data.items():
            pid = query_id.split("_")[2]
            v3_pool = value[1]
            result[v3_pool] = {
                "farming_pid": pid,
                "token0": value[2],
                'token1': value[3],
                'fee': value[4],
                'stake_liquidity': value[5],
            }

        return result

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        multicall_calls: List['W3Multicall.Call'] = []
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for fn_name in ["liquidity", "slot0", 'tickSpacing']:
                multicall_calls.append(W3Multicall.Call(
                    address=lp_token, abi=self.pool_info['pool_abi'], fn_name=fn_name, block_number=block_number))

            for token_key in ['token0', 'token1']:
                token_address = value.get(token_key)
                multicall_calls.append(W3Multicall.Call(
                    address=token_address, abi=ERC20_ABI, fn_name="decimals", block_number=block_number))
                multicall_calls.append(W3Multicall.Call(
                    address=lp_token, abi=self.pool_info['pool_abi'], fn_name=token_key, block_number=block_number))

        return multicall_calls

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            slot0 = response_data.get(f"slot0_{lp_token}_{block_number}".lower())
            token0_address = value.get('token0')
            token1_address = value.get('token1')
            if token0_address == response_data.get(f'token0_{lp_token}_{block_number}'.lower()):
                token0_decimals = response_data.get(f'decimals_{token0_address}_{block_number}'.lower())
                token1_decimals = response_data.get(f'decimals_{token1_address}_{block_number}'.lower())
            else:
                token1_decimals = response_data.get(f'decimals_{token0_address}_{block_number}'.lower())
                token0_decimals = response_data.get(f'decimals_{token1_address}_{block_number}'.lower())
            price = (slot0[0] / 2 ** 96) ** 2 * 10 ** (token0_decimals - token1_decimals)
            unstake_liquidity = response_data.get(f"liquidity_{lp_token}_{block_number}".lower())
            tick_spacing = response_data.get(f'tickSpacing_{lp_token}_{block_number}'.lower())

            lp_token_info[lp_token].update({
                "token0": token0_address,
                "token1": token1_address,
                'liquidity_in_range': unstake_liquidity,
                "price": price,
                'tick': slot0[1],
                'tick_spacing': tick_spacing,
                'token0_decimals': token0_decimals,
                'token1_decimals': token1_decimals,
            })
        return lp_token_info

    def decode_balance_of_token_function_info(
            self, supplied_data, decoded_data, block_number: int = "latest"):
        lp_token_info = {}
        for lp_token, value in supplied_data['lp_token_info'].items():
            lp_token_info[lp_token] = copy.deepcopy(value)
            liquidity_in_range = value.get('liquidity_in_range')
            for token_key in ["token0", "token1"]:
                token_address = value.get(token_key, None)
                decimals = decoded_data.get(f'decimals_{token_address}_{block_number}'.lower())
                if token_address is not None:
                    balance_of = decoded_data.get(
                        f'balanceOf_{token_address}_{lp_token}_{block_number}'.lower()) / 10 ** decimals
                    lp_token_info[lp_token].update({
                        f'{token_key}_amount': balance_of,
                        # f'{token_key}AmountStake': balance_of / liquidity_in_range * stake_liquidity
                    })

            tick = value.get('tick')
            tick_spacing = value.get('tick_spacing')
            tick_lower = tick // tick_spacing * tick_spacing
            tick_upper = (tick // tick_spacing + 1) * tick_spacing
            amount0, amount1 = get_token_amount_of_pool(liquidity=liquidity_in_range,
                                                        tick_lower=tick_lower, tick_upper=tick_upper)
            # stake_amount0, stake_amount1 = get_token_amount_of_pool(liquidity=value.get("stake_liquidity"), tick_lower= tick_lower, tick_upper=tick_upper)
            lp_token_info[lp_token].update({
                'token0_amount_in_range': amount0 / 10 ** value.get('token0_decimals'),
                'token1_amount_in_range': amount1 / 10 ** value.get('token1_decimals'),
                # 'token0_amount_stake': stake_amount0 / 10 ** value.get('token0_decimals'),
                # 'token1_amount_stake': stake_amount1 / 10 ** value.get('token1_decimals')
            })

        return lp_token_info

    ### USER
    def get_all_nft_token_of_user_function(
            self, user: str, block_number: int = "latest"):
        multicall_calls = super().get_all_nft_token_of_user_function(user, block_number)
        user = self.web3.to_checksum_address(user)
        self.masterchef_addr = self.web3.to_checksum_address(self.masterchef_addr)
        master_chef_contract = self.web3.eth.contract(abi=self.masterchef_abi, address=self.masterchef_addr)
        number_stake_nft_token = master_chef_contract.functions.balanceOf(user).call()
        for idx in range(number_stake_nft_token):
            multicall_calls.append(W3Multicall.Call(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[self.web3.to_checksum_address(user), idx], block_number=block_number))

        return multicall_calls

    def decode_all_nft_token_of_user_function(
            self, decode_data: dict):
        result = {'all_token': super().decode_all_nft_token_of_user_function(decode_data), 'stake_token': {}}

        for query_id, token_id in decode_data.items():
            contract_addr = query_id.split("_")[1]
            if contract_addr == self.masterchef_addr.lower():
                result['stake_token'][token_id] = {}

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = True, block_number: int = "latest"):
        supplied_param = {'user_data': supplied_data['user_data']['all_token']}
        multicall_calls = super().get_user_info_function(user, supplied_param, stake, block_number)

        for token_id, value in supplied_data['user_data']['stake_token'].items():
            multicall_calls.append(W3Multicall.Call(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="userPositionInfos",
                fn_paras=[int(token_id)]))
            multicall_calls.append(W3Multicall.Call(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="pendingCake", fn_paras=int(token_id)))
            multicall_calls.append(W3Multicall.Call(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="positions",
                fn_paras=int(token_id)))

        return multicall_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict = None,
                                  stake: bool = True,
                                  block_number: int = "latest"):
        supplied_param = {'user_data': supplied_data['user_data'].get('all_token')}
        user_data_with_liquidity = {
            'all_token': super().decode_user_info_function(user, supplied_param, decoded_data, stake,
                                                           block_number), 'stake_token': {}}

        for token_id, value in supplied_data['user_data'].get('stake_token').items():
            master_chef_position = decoded_data.get(
                f'userPositionInfos_{self.masterchef_addr}_{token_id}_{block_number}'.lower())
            liquidity = master_chef_position[0]
            if liquidity > 0:
                nft_position = decoded_data.get(
                    f'positions_{self.nft_token_manager_addr}_{token_id}_{block_number}'.lower())
                user_data_with_liquidity['stake_token'][token_id] = {
                    'liquidity': master_chef_position[0],
                    'tick_lower': master_chef_position[2],
                    'tick_upper': master_chef_position[3],
                    'reward': master_chef_position[5] / 10 ** 18,
                    'farming_pid': master_chef_position[7],
                    'reward_token': self.pool_info['reward_token'],
                    'pending_cake': decoded_data.get(
                        f'pendingCake_{self.masterchef_addr}_{token_id}_{block_number}'.lower()) / 10 ** 18,
                    'fee_growth_inside0_x128': nft_position[8],
                    'fee_growth_inside1_x128': nft_position[9],
                }

        return user_data_with_liquidity

    def get_user_token_amount_function(self, user: str, supplied_data: dict, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        supplied_param = {'user_data': user_data['all_token']}
        multicall_calls = super().get_user_token_amount_function(user, supplied_param, block_number)
        for token_id, value in supplied_data['user_data']['stake_token'].items():
            pid = value.get('farming_pid')
            multicall_calls.append(W3Multicall.Call(
                address=self.masterchef_addr, abi=self.masterchef_abi, fn_name="poolInfo", fn_paras=pid))

        return multicall_calls

    def decode_user_token_amount_function(self, user: str, supplied_data: dict, decoded_data: dict = None,
                                          block_number: int = "latest"):
        user_data = supplied_data['user_data']
        lp_token_info = supplied_data['lp_token_info']
        supplied_param = {'user_data': user_data['all_token'],
                          'lp_token_info': lp_token_info}
        user_data['all_token'] = super().decode_user_token_amount_function(user, supplied_param, decoded_data,
                                                                           block_number)
        for token_id, value in user_data['stake_token'].items():
            pid = value.get('farming_pid')
            pool_info = decoded_data.get(f'poolInfo_{self.masterchef_addr}_{pid}_{block_number}'.lower())
            lp_token_address = pool_info[1]
            user_data['stake_token'][token_id].update({
                'pool_address': lp_token_address,
                'token0': pool_info[2],
                'token1': pool_info[3],
                'fee': pool_info[4]
            })
            liquidity = value.get('liquidity')
            token0_decimals = lp_token_info.get(lp_token_address, {}).get("token0_decimals")
            token1_decimals = lp_token_info.get(lp_token_address, {}).get("token1_decimals")
            price = lp_token_info.get(lp_token_address, {}).get("price")
            tick = lp_token_info.get(lp_token_address, {}).get('tick')
            tick_lower = value.get('tick_lower')
            tick_upper = value.get('tick_upper')
            if price and tick:
                sqrt_price_x96 = (math.sqrt(price / 10 ** (token0_decimals - token1_decimals))) * 2 ** 96
                token0_amount, token1_amount = get_token_amount_of_user(liquidity=liquidity,
                                                                        sqrt_price_x96=sqrt_price_x96,
                                                                        tick=tick, tick_upper=tick_upper,
                                                                        tick_lower=tick_lower)
                user_data['stake_token'][token_id].update(
                    {
                        'token0_amount': token0_amount / 10 ** token0_decimals,
                        'token1_amount': token1_amount / 10 ** token1_decimals,
                    }
                )
        return user_data

    def get_rewards_balance_function_info(self, user, supplied_data, block_number: int = "latest"):
        user_data = supplied_data['user_data']
        supplied_param = {'user_data': user_data['all_token']}
        multicall_calls = super().get_rewards_balance_function_info(user, supplied_param, block_number)
        for token_id, value in supplied_data['user_data']['stake_token'].items():
            lp_token_address = value.get('pool_address')
            tick_lower = value.get('tick_lower')
            tick_upper = value.get('tick_upper')
            for fn_name in ['feeGrowthGlobal0X128', 'feeGrowthGlobal1X128']:
                multicall_calls.append(W3Multicall.Call(
                    address=lp_token_address, abi=self.pool_info['pool_abi'], fn_name=fn_name))

            for param in [tick_lower, tick_upper]:
                multicall_calls.append(W3Multicall.Call(
                    address=lp_token_address, abi=self.pool_info['pool_abi'], fn_name="ticks", fn_paras=param))

        return multicall_calls

    def calculate_rewards_balance(
            self, user: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest"):
        lp_token_info = supplied_data['lp_token_info']
        user_data = supplied_data['user_data']

        supplied_param = {'user_data': user_data['all_token'],
                          'lp_token_info': lp_token_info}
        user_data['all_token'] = super().calculate_rewards_balance(user, supplied_param, decoded_data, block_number)
        for token_id, value in user_data['stake_token'].items():
            lp_token_address = value.get('pool_address')
            tick_lower = value.get('tick_lower')
            tick_upper = value.get('tick_upper')
            fee_growth_inside_0_x128 = value.get('fee_growth_inside0_x128')
            fee_growth_inside_1_x128 = value.get('fee_growth_inside1_x128')
            fee_growth_global_0 = decoded_data.get(f'feeGrowthGlobal0X128_{lp_token_address}_{block_number}'.lower())
            fee_growth_global_1 = decoded_data.get(f'feeGrowthGlobal1X128_{lp_token_address}_{block_number}'.lower())
            fee_growth_0_low_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_lower}_{block_number}'.lower())[2]
            fee_growth_1_low_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_lower}_{block_number}'.lower())[3]
            fee_growth_0_hi_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_upper}_{block_number}'.lower())[2]
            fee_growth_1_hi_x128 = decoded_data.get(f'ticks_{lp_token_address}_{tick_upper}_{block_number}'.lower())[3]
            liquidity = value.get('liquidity')
            token0_decimals = lp_token_info.get(lp_token_address, {}).get("token0_decimals")
            token1_decimals = lp_token_info.get(lp_token_address, {}).get("token1_decimals")
            tick = lp_token_info.get(lp_token_address, {}).get('tick')
            if tick and token0_decimals and token1_decimals:
                token0_reward, token1_reward = get_fees(
                    fee_growth_global_0=fee_growth_global_0,
                    fee_growth_global_1=fee_growth_global_1,
                    fee_growth_0_low=fee_growth_0_low_x128,
                    fee_growth_1_low=fee_growth_1_low_x128,
                    fee_growth_0_hi=fee_growth_0_hi_x128,
                    fee_growth_1_hi=fee_growth_1_hi_x128,
                    fee_growth_inside_0=fee_growth_inside_0_x128,
                    fee_growth_inside_1=fee_growth_inside_1_x128,
                    liquidity=liquidity, tick_lower=tick_lower,
                    tick_upper=tick_upper, tick_current=tick,
                    decimals0=token0_decimals, decimals1=token1_decimals)

                user_data['stake_token'][token_id].update({
                    'token0_reward': token0_reward,
                    'token1_reward': token1_reward
                })

        return user_data
