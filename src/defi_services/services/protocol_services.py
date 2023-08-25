class ProtocolServices:
    def get_service_info(self):
        # Get basic information of service
        pass

    def get_dapp_asset_info(self, block_number: int = 'latest'):
        # Get asset information of protocol
        pass

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
        # Get final result or process response data
        pass

    def get_token_list(self):
        # Get necessary tokens related to protocol
        pass
