class ProtocolServices:
    def get_function_info(
            self,
            query_types: list,
            wallet: str = None,
            block_number: int = "latest",
            **kwargs
    ):
        # Get rpc calls information
        pass

    def get_data(
            self,
            query_types: list,
            wallet: str,
            decoded_data: dict,
            block_number: int = 'latest',
            **kwargs
    ):
        # Get final result
        pass

    def get_token_list(self):
        # Get necessary tokens
        pass

    def get_token_prices(self, tokens):
        # Get token prices
        pass

