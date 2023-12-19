import logging

from substrateinterface import SubstrateInterface
from defi_services.constants.query_constant import Query

logger = logging.getLogger("SubstrateStateQuerier")


class SubstrateStateQuerier:
    def __init__(self, provider_uri):
        self.provider_uri = provider_uri
        self.client_querier = SubstrateInterface(provider_uri)

    def get_client_querier(self):
        return self.client_querier

    @staticmethod
    def get_function_info(module: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        if fn_paras is None:
            fn_paras = []
        data = {
            "module": module,
            "function": fn_name,
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
                        function: str - name of the function,
                        params: list - list parameters of function
                    }
            batch_size: int - number of query in each batch queries
            workers: int - maximum number of vCPU used in queries
            ignore_error: bool - ignore error when decode result or not

        Return:
            + A dictionary result of queries
                - key: str - id of query
                - value: result of query
        """
        block_hash, rpc_call, list_call_id = {}, {}, []
        for key, value in queries.items():
            module = value.get(Query.module)
            fn_paras = value.get(Query.params)
            fn_name = value.get(Query.function)
            block_number = value.get(Query.block_number)
            if block_number not in rpc_call:
                rpc_call[block_number] = []
            if block_number != "latest" and block_number not in block_hash:
                block_hash[block_number] = self.client_querier.get_block_hash(block_number)
            eth_call = self.add_rpc_call(module=module, fn_name=fn_name, fn_paras=fn_paras)
            list_call_id.append(key)
            rpc_call[block_number].append(eth_call)

        # TODO: query by batch with batch size and workers

        decoded_data = {}
        for block_number, list_rpc_call in rpc_call.items():
            try:
                if block_number != "latest":
                    response_data = self.client_querier.query_multi(list_rpc_call, block_hash.get(block_number))
                else:
                    response_data = self.client_querier.query_multi(list_rpc_call)

                decoded_data.update(self.decode_response_data(response_data, block_number))
            except Exception as e:
                if not ignore_error:
                    logger.error(f"An exception when decode data from provider: {e}")
                    raise
                else:
                    logger.error(f"[Ignored] An exception when decode data from provider: {e}")
                    continue

        return decoded_data

    def add_rpc_call(self, module: str, fn_name: str, fn_paras: list = None):
        call = self.client_querier.create_storage_key(module, fn_name, fn_paras)
        return call

    @staticmethod
    def decode_response_data(response_data: list, block_number: int = "latest"):
        decoded_data = {}
        for data in response_data:
            storage_key = data[0]
            storage_value = data[1]
            key = f"{storage_key.pallet}_{storage_key.storage_function}_{storage_key.params}_{block_number}".lower()
            value = storage_value.value_serialized
            decoded_data[key] = value

        return decoded_data
