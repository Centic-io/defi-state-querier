import logging

from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token

logger = logging.getLogger("Dex Protocol State Service")


class DexProtocolServices:
    # BASIC FUNCTIONS
    def get_service_info(self):
        # Get basic information of service
        return {}

    def get_function_info(
            self,
            query_types: list,
            wallet: str = None,
            block_number: int = "latest",
            **kwargs
    ):
        rpc_calls = {}
        lp_token_info = kwargs.get("lp_token_info", {})
        if Query.lp_token_list in query_types:
            limit_ = kwargs.get("number_lp", 0)
            rpc_calls.update(self.get_all_supported_lp_token(limit_))
        if Query.lp_token_info in query_types:
            lp_token_list = {key: value.get("pid") for key, value in lp_token_info}
            rpc_calls.update(self.get_lp_token_function_info(lp_token_list, block_number))
        if Query.dex_user_info in query_types and wallet and wallet != Token.native_token:
            stake = kwargs.get("stake", False)
            rpc_calls.update(self.get_user_info_function(wallet, lp_token_info, stake, block_number))
        if Query.token_pair_balance:
            rpc_calls.update(self.get_balance_of_token_function_info(lp_token_info, block_number))
        if Query.protocol_reward in query_types and wallet and wallet != Token.native_token:
            rpc_calls.update(self.get_rewards_balance_function_info(wallet, lp_token_info, block_number))

        return rpc_calls

    def get_data(
            self,
            query_types: list,
            wallet: str,
            decoded_data: dict,
            block_number: int = 'latest',
            **kwargs
    ):
        result = {}
        lp_token_info = kwargs.get("lp_token_info", {})
        stake = kwargs.get("stake", False)
        token_price = kwargs.get("token_price", {})
        if Query.lp_token_list in query_types:
            result.update(self.decode_all_supported_lp_token(decoded_data))
        if Query.lp_token_info in query_types:
            lp_token_list = {key: value.get("pid") for key, value in lp_token_info}
            result.update(self.decode_lp_token_info(lp_token_list, block_number))
        if Query.dex_user_info in query_types and wallet and wallet != Token.native_token:
            result.update(self.decode_user_info_function(
                wallet, lp_token_info, decoded_data, token_price, stake, block_number))
        if Query.token_pair_balance:
            result.update(self.decode_balance_of_token_function_info(
                lp_token_info, decoded_data, token_price, block_number))
        if Query.protocol_reward:
            result.update(self.calculate_rewards_balance(wallet, lp_token_info, decoded_data, block_number))

        return result

    # Lp token liquidity
    def get_balance_of_token_function_info(self, lp_token_info, block_number: int = "latest"):
        return {}

    def decode_balance_of_token_function_info(
            self, lp_token_info, balance_info, token_price, block_number: int = "latest"):
        return {}

    # User information
    def get_user_info_function(self, user: str, lp_token_info: dict, stake: bool = True, block_number: int = "latest"):
        return {}

    def decode_user_info_function(
            self, user: str, lp_token_info: dict, user_data: dict, token_price: dict = None, stake: bool = True,
            block_number: int = "latest"):
        return {}

    # Lp token function
    def get_lp_token_function_info(self, lp_token_list, block_number: int = "latest"):
        return {}

    def decode_lp_token_info(self, lp_token_list, response_data, block_number: int = "latest"):
        return {}

    # Get lp list
    def get_all_supported_lp_token(self, limit: int = 10):
        return {}

    def decode_all_supported_lp_token(self, response_data):
        return {}

    # Reward
    def get_rewards_balance_function_info(self, user, lp_token_info, block_number: int = "latest"):
        return {}

    def calculate_rewards_balance(
            self,
            wallet: str,
            lp_token_info: dict,
            decoded_data: dict,
            block_number: int = "latest"
    ) -> dict:
        return {}
