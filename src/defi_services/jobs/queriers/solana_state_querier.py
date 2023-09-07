import logging

from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from query_state_lib.client.client_querier import ClientQuerier

from defi_services.constants.query_constant import Query

logger = logging.getLogger("SolanaStateQuerier")


class SolanaStateQuerier:
    def __init__(self, provider_uri):
        self.provider_uri = provider_uri
        self.client_querier = ClientQuerier(provider_url=provider_uri)

    @staticmethod
    def get_function_info(fn_name: str, fn_paras: list = None):
        if fn_paras is None:
            fn_paras = []
        data = {
            "function": fn_name,
            "params": fn_paras
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
        list_rpc_call, list_call_id = [], []
        for key, value in queries.items():
            fn_paras = value.get(Query.params)
            fn_name = value.get(Query.function)
            eth_call = self.add_rpc_call(fn_name=fn_name, fn_paras=fn_paras, call_id=key)
            list_call_id.append(key)
            list_rpc_call.append(eth_call)

        response_data = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size, workers)
        decoded_data = self.decode_response_data(response_data, list_call_id, ignore_error=ignore_error)
        return decoded_data

    @staticmethod
    def add_rpc_call(fn_name: str, fn_paras: list = None, call_id: str = None):
        solana_call = EthJsonRpc(method=fn_name, params=fn_paras, id=call_id)
        return solana_call

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
