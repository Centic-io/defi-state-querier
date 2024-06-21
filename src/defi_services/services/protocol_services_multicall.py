import logging
import time
from typing import List

from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token
from defi_services.services.blockchain.multicall_v2 import W3Multicall

logger = logging.getLogger("Lending Pool State Service")


class ProtocolServices:
    def __init__(self):
        self.chain_id = None
        self.pool_info = {}

    # BASIC FUNCTIONS
    def get_service_info(self):
        # Get basic information of service
        return {}

    def get_dapp_asset_info(self, block_number: int = 'latest'):
        # Get asset information of protocol
        return {}

    def get_token_list(self):
        begin = time.time()
        reward_token = self.pool_info.get('rewardToken')
        tokens = [self.pool_info.get("poolToken")]
        if isinstance(reward_token, list):
            tokens += reward_token
        elif isinstance(reward_token, str):
            tokens.append(reward_token)

        for token in self.pool_info.get("reservesList"):
            if token == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
                continue
            tokens.append(token)
        logger.info(f"Get token list related in {time.time() - begin}s")
        tokens = list(set(tokens))
        return tokens

    def get_function_info(
            self,
            query_types: list,
            wallet: str = None,
            block_number: int = "latest",
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", self.pool_info.get("reservesList"))
        multicall_calls: List['W3Multicall.Call'] = []

        if Query.deposit_borrow in query_types and wallet and wallet != Token.native_token:
            multicall_calls.extend(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number
            ))

        if Query.protocol_reward in query_types and wallet and wallet != Token.native_token:
            multicall_calls.extend(self.get_rewards_balance_function_info(wallet, reserves_info, block_number))

        if Query.deposit_borrow_health_factor in query_types:
            multicall_calls.extend(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number, health_factor=True
            ))
        if Query.health_factor in query_types:
            multicall_calls.extend(self.get_health_factor_function_info(wallet, reserves_info, block_number))

        if Query.protocol_apy in query_types:
            multicall_calls.extend(self.get_apy_lending_pool_function_info(reserves_info, block_number))

        if Query.staking_reward in query_types and wallet and wallet != Token.native_token:
            multicall_calls.extend(self.get_wallet_staking_balance_function_info(
                wallet, reserves_info, block_number, return_reward=True
            ))

        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return multicall_calls

    def get_data(
            self,
            query_types: list,
            wallet: str,
            decoded_data: dict,
            block_number: int = 'latest',
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", self.pool_info.get("reservesList"))
        token_prices = kwargs.get("token_prices", {})
        pool_token_price = token_prices.get(self.pool_info.get('poolToken'), 1)
        pool_decimals = kwargs.get("pool_decimals", 18)
        result = {}
        if Query.deposit_borrow in query_types and wallet and wallet != Token.native_token:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, pool_decimals,
                block_number
            ))

        if Query.protocol_reward in query_types and wallet and wallet != Token.native_token:
            result.update(self.calculate_rewards_balance(
                wallet, reserves_info, decoded_data, block_number
            ))

        if Query.health_factor in query_types:
            result.update(self.calculate_health_factor(
                wallet, reserves_info, decoded_data, token_prices, pool_decimals, block_number))

        if Query.deposit_borrow_health_factor in query_types:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, pool_decimals,
                block_number, health_factor=True
            ))

        if Query.protocol_apy in query_types:
            result.update(self.calculate_apy_lending_pool_function_call(
                reserves_info, decoded_data, token_prices, pool_token_price, pool_decimals, block_number))

        if Query.staking_reward in query_types and wallet and wallet != Token.native_token:
            result.update(self.calculate_wallet_staking_balance(
                wallet, reserves_info, decoded_data, token_prices, block_number, return_reward=True
            ))

        logger.info(f"Process protocol data in {time.time() - begin}")
        return result

    # REWARD BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest"
    ) -> dict:
        return {}

    def calculate_rewards_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            block_number: int = "latest"
    ) -> dict:
        return {}

    # DEPOSIT BORROW
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            health_factor: bool = False
    ) -> dict:
        return {}

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_decimals: int = 18,
            block_number: int = 'latest',
            health_factor: bool = False
    ) -> dict:
        return {}

    # HEALTH FACTOR
    def get_health_factor_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        return {}

    def calculate_health_factor(
            self,
            wallet: str,
            reserves_info,
            decoded_data: dict = None,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest"
    ):
        return {}

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
    ) -> dict:
        ...

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ) -> dict:
        ...

    # CALCULATE WALLET STAKING BALANCE
    def get_wallet_staking_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            return_reward: bool = False
    ) -> dict:
        ...

    def calculate_wallet_staking_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            block_number: int = 'latest',
            return_reward: bool = False
    ) -> dict:
        ...
