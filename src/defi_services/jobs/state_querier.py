import logging

from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.mappers.get_balance_mapper import GetBalance
from query_state_lib.base.utils.encoder import encode_eth_call_data
from query_state_lib.client.client_querier import ClientQuerier
from web3 import Web3
from web3.middleware import geth_poa_middleware

from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token

logger = logging.getLogger("StateService")


class StateQuerier:
    def __init__(self, provider_uri):
        self.provider_uri = provider_uri
        self._w3 = Web3(Web3.HTTPProvider(provider_uri))
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.client_querier = ClientQuerier(provider_url=provider_uri)

    def get_w3(self):
        return self._w3

    @staticmethod
    def get_function_info(address: str, abi: list, fn_name: str, fn_paras: list = None, block_number: int = 'latest'):
        if fn_paras is None:
            fn_paras = []
        data = {
            "address": address,
            "abi": abi,
            "function": fn_name,
            "params": fn_paras,
            "block_number": block_number
        }

        return data

    @staticmethod
    def get_native_token_balance_info(fn_paras: str = None, block_number: int = 'latest'):
        data = {
            "params": fn_paras,
            "block_number": block_number
        }
        return data

    def query_state_data(self, queries: dict, batch_size: int = 100, workers: int = 5, ignore_error: bool = False):
        """
        Args:
            queries: dict - defi state queries
                - key: str - id of query
                - value: dict - input of query
                    {
                        address: str - address of contract
                        abi: list - abi of contract,
                        function: str - name of the function,
                        params: list - list parameters of function,
                        block_number: int - the block number saving the state data
                    }
            batch_size: int - number of query in each batch queries
            workers: int - maximum number of vCPU used in queries
            ignore_error: bool - ignore error when decode result or not

        Return:
            + A dictionary result of queries
                - key: str - id of query
                - value: result of query
        """
        list_rpc_call, list_call_id = [], []
        for key, value in queries.items():
            fn_paras = value.get(Query.params)
            block_number = value.get(Query.block_number)
            if Token.native_token in key and "balanceof" in key:
                eth_call = self.add_native_token_balance_rpc_call(fn_paras, key, block_number)
            else:
                abi = value.get(Query.abi)
                contract_address = value.get(Query.address)
                fn_name = value.get(Query.function)
                if not block_number or block_number == 'latest':
                    eth_call = self.add_rpc_call(
                        abi=abi, fn_name=fn_name, contract_address=contract_address,
                        fn_paras=fn_paras, call_id=key
                    )
                else:
                    eth_call = self.add_rpc_call(
                        abi=abi, fn_name=fn_name, contract_address=contract_address,
                        block_number=block_number, fn_paras=fn_paras, call_id=key
                    )
            list_call_id.append(key)
            list_rpc_call.append(eth_call)

        response_data = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size, workers)
        decoded_data = self.decode_response_data(response_data, list_call_id, ignore_error=ignore_error)
        return decoded_data

    def add_native_token_balance_rpc_call(
            self, fn_paras: str = None, call_id: str = None, block_number: int = "latest"):
        eth_call = GetBalance(Web3.toChecksumAddress(fn_paras), block_number, call_id)
        return eth_call

    def add_rpc_call(self, abi: dict, fn_name: str, contract_address: str,
                     fn_paras: list = None, call_id: str = None, block_number: int = "latest"):
        args = []
        if fn_paras:
            for item in fn_paras:
                if self._w3.isAddress(item):
                    item = self._w3.toChecksumAddress(item)
                args.append(item)

        data_call = encode_eth_call_data(abi=abi, fn_name=fn_name, args=args)
        eth_call = EthCall(to=self._w3.toChecksumAddress(contract_address), block_number=block_number, data=data_call,
                           abi=abi, fn_name=fn_name, id=call_id)
        return eth_call

    @staticmethod
    def decode_response_data(response_data: dict, list_call_id: list, ignore_error=False):
        decoded_data = {}
        for call_id in list_call_id:
            try:
                response_datum = response_data.get(call_id)
                decoded_datum = response_datum.decode_result()
            except Exception as e:
                if not ignore_error:
                    logger.error(f"An exception when decode data from provider: {e}")
                    raise
                else:
                    logger.error(f"[Ignored] An exception when decode data from provider: {e}")
                    continue
            if isinstance(decoded_datum, int):
                decoded_data[call_id] = decoded_datum
            elif len(decoded_datum) == 1:
                decoded_data[call_id] = decoded_datum[0]
            else:
                decoded_data[call_id] = decoded_datum
        return decoded_data
