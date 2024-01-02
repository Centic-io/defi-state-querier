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
        supplied_data = kwargs.get("supplied_data", {})

        if Query.lp_token_list in query_types:
            limit_ = kwargs.get("number_lp")
            rpc_calls.update(self.get_all_supported_lp_token(limit_, supplied_data))

        if Query.farming_lp_token_list in query_types:
            limit_ = kwargs.get("number_lp")
            rpc_calls.update(self.get_farming_supported_lp_token(limit_))
        if Query.important_lp_token_list in query_types:
            rpc_calls.update(self.get_important_lp_token(supplied_data,block_number))

        if Query.lp_token_info in query_types:
            rpc_calls.update(self.get_lp_token_function_info(supplied_data, block_number))

        if Query.token_pair_balance in query_types:
            rpc_calls.update(self.get_balance_of_token_function_info(supplied_data, block_number))

        if Query.dex_user_nft in query_types and wallet and wallet != Token.native_token:
            rpc_calls.update(self.get_all_nft_token_of_user_function(wallet, block_number))

        if Query.dex_user_info in query_types and wallet and wallet != Token.native_token:
            stake = kwargs.get("stake", False)
            rpc_calls.update(self.get_user_info_function(wallet, supplied_data, stake, block_number))

        if Query.protocol_reward in query_types and wallet and wallet != Token.native_token:
            rpc_calls.update(self.get_rewards_balance_function_info(wallet, supplied_data, block_number))

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
        supplied_data = kwargs.get("supplied_data", {})
        if Query.lp_token_list in query_types:
            result.update(self.decode_all_supported_lp_token(decoded_data, supplied_data))

        if Query.farming_lp_token_list in query_types:
            result.update(self.decode_farming_supported_lp_token(decoded_data))

        if Query.important_lp_token_list in query_types:
            result.update(self.decode_important_lp_token(supplied_data, decoded_data))

        if Query.lp_token_info in query_types:
            result.update(self.decode_lp_token_info(supplied_data, decoded_data, block_number))

        if Query.token_pair_balance in query_types:
            result.update(self.decode_balance_of_token_function_info(
                supplied_data, decoded_data, block_number))

        if Query.dex_user_nft in query_types and wallet and wallet != Token.native_token:
            result.update(self.decode_all_nft_token_of_user_function(decoded_data))

        if Query.dex_user_info in query_types and wallet and wallet != Token.native_token:
            stake = kwargs.get("stake", False)
            result.update(self.decode_user_info_function(wallet, supplied_data, decoded_data, stake, block_number))

        if Query.protocol_reward in query_types and wallet and wallet != Token.native_token:
            result.update(self.calculate_rewards_balance(wallet, supplied_data, decoded_data, block_number))

        return result

    # Lp token function
    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest") -> dict:
        pass

    def decode_lp_token_info(self, supplied_data, decoded_data, block_number: int = "latest") -> dict:
        pass

    # Get lp list
    def get_all_supported_lp_token(self, limit: int = 10, supplied_data:dict = None) -> dict:
        pass

    def decode_all_supported_lp_token(self, decoded_data, supplied_data:dict = None) -> dict:
        pass

    # Get farming supported lp list
    def get_farming_supported_lp_token(self, limit: int = 10) -> dict:
        pass

    def decode_farming_supported_lp_token(self, decoded_data) -> dict:
        pass

    def get_important_lp_token(self, supplied_data,block_number) -> dict:
        pass

    def decode_important_lp_token(self, supplied_data, decoded_data) ->dict:
        pass

    # Lp token liquidity
    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest") -> dict:
        pass

    def decode_balance_of_token_function_info(
            self, supplied_data, decoded_data, block_number: int = "latest") -> dict:
        pass

    # User information
    def get_user_info_function(self, wallet: str, supplied_data: dict, stake: bool = True, block_number: int = "latest") -> dict:
        pass

    def decode_user_info_function(
            self, wallet: str, supplied_data: dict, user_data: dict, stake: bool = True,
            block_number: int = "latest") -> dict:
        pass

    def get_all_nft_token_of_user_function(
            self, wallet: str, block_number: int = "latest") -> dict:
        pass

    def decode_all_nft_token_of_user_function(
            self, decode_data: dict) -> dict:
        pass

    # User reward
    def get_rewards_balance_function_info(self, wallet, supplied_data, block_number: int = "latest") -> dict:
        pass

    def calculate_rewards_balance(
            self, wallet: str, supplied_data: dict, decoded_data: dict, block_number: int = "latest") -> dict:
        pass

    @staticmethod
    def get_token_list() -> list:
        return []
