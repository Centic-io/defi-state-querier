import logging

from web3 import Web3

from defi_services.abis.multicall_v3_abi import MULTICALL_V3_ABI
from defi_services.constants.network_constants import MulticallContract
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.multicall.batch_queries_service import decode_data_response_ignore_error, \
    decode_data_response
from defi_services.services.multicall.multicall_v2 import W3Multicall, add_rpc_multicall

logger = logging.getLogger("CallStateQuerier")


class CallStateQuerier(StateQuerier):
    def __init__(self, provider_uri, chain_id):
        super().__init__(provider_uri)
        self.chain_id = chain_id
        self.multicall_address = Web3.to_checksum_address(MulticallContract.get_multicall_contract(self.chain_id))

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
        w3_multicall = W3Multicall(self._w3, address=self.multicall_address)
        for key, value in queries.items():
            fn_paras = value.get(Query.params)
            block_number = value.get(Query.block_number)
            items = key.split('_')
            if (not value.get(Query.address) or value.get(Query.address) == Token.native_token) and "balanceof" == items[0]:
                w3_multicall.add(W3Multicall.Call(
                    self.multicall_address, MULTICALL_V3_ABI, fn_paras=fn_paras,
                    fn_name="getEthBalance", block_number=block_number, key=key
                ))
            else:
                abi = value.get(Query.abi)
                contract_address = value.get(Query.address)
                checksum_address = Web3.to_checksum_address(contract_address)
                fn_name = value.get(Query.function)
                w3_multicall.add(W3Multicall.Call(
                    checksum_address, abi, fn_name=fn_name,
                    fn_paras=fn_paras,
                    block_number=block_number, key=key
                ))

        list_call_id, list_rpc_call = [], []
        add_rpc_multicall(
            w3_multicall,
            list_rpc_call=list_rpc_call, list_call_id=list_call_id,
            batch_size=batch_size
        )
        response_data = self.client_querier.sent_batch_to_provider(list_rpc_call, 1, workers)
        filtered_response_data = {}
        # loại bỏ những phần tử không có data
        for key, value in response_data.items():
            if value is not None:
                filtered_response_data[key] = value
            else:
                logger.info(key)
        filtered_keys = list(filtered_response_data.keys())
        response_data = filtered_response_data
        list_call_id = [call_id for call_id in list_call_id if call_id in filtered_keys]
        decoded_data = self.decode_response_data(
            response_data, list_call_id, ignore_error=ignore_error, w3_multicall=w3_multicall, batch_size=batch_size)
        return decoded_data

    def decode_response_data(
            self, response_data: dict, list_call_id: list, ignore_error=False, w3_multicall=None, batch_size=100):
        if ignore_error:
            decoded_data = decode_data_response_ignore_error(data_responses=response_data, list_call_id=list_call_id)
        else:
            decoded_data = decode_data_response(data_responses=response_data, list_call_id=list_call_id)
        batch_idx = 0
        results = {}
        for block_number, batch_calls in w3_multicall.batch_calls_iterator(batch_size=batch_size):
            multicall_data = decoded_data.get(f'{batch_idx}_{block_number}')
            decode_multicall_data = w3_multicall.decode(multicall_data, calls=batch_calls, ignore_error=ignore_error)
            results.update(decode_multicall_data)
            batch_idx += 1

        return results
