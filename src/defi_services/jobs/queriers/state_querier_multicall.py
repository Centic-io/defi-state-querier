import logging
from typing import List

from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.mappers.get_balance_mapper import GetBalance
from query_state_lib.client.client_querier import ClientQuerier
from web3 import Web3, contract
from web3.middleware import geth_poa_middleware

from defi_services.abis.multicall_v3_abi import MULTICALL_V3_ABI
from defi_services.constants.network_constants import MulticallContract
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token, ProtocolNFT
from defi_services.services.blockchain.multicall_v2 import W3Multicall, add_rpc_multicall, decode_multical_response
from defi_services.utils.thread_proxy import ThreadLocalProxy, get_provider_from_uri

logger = logging.getLogger("StateQuerier")


class StateQuerier:
    def __init__(self, provider_uri, chain_id):
        self.provider_uri = provider_uri
        self._w3 = Web3(Web3.HTTPProvider(provider_uri))
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.client_querier = ClientQuerier(provider_url=provider_uri)
        self.multicall_contract = Web3.to_checksum_address(MulticallContract.get_multicall_contract(chain_id))
        self.w3_multicall = W3Multicall(web3=self._w3, address=self.multicall_contract)

    def get_w3(self):
        return self._w3

    # def get_client_querier(self):
    #     return self.client_querier

    # @staticmethod
    # def get_function_info(address: str, abi: list, fn_name: str, fn_paras: list = None, block_number: int = 'latest'):
    #     if fn_paras is None:
    #         fn_paras = []
    #     data = {
    #         "address": address,
    #         "abi": abi,
    #         "function": fn_name,
    #         "params": fn_paras,
    #         "block_number": block_number
    #     }
    #
    #     return data

    @staticmethod
    def get_native_token_balance_info(fn_paras: str = None, block_number: int = 'latest'):
        data = {
            "params": fn_paras,
            "block_number": block_number
        }
        return data

    def query_state_data(self, queries: List['W3Multicall.Call'], batch_size: int = 100, workers: int = 5, ignore_error: bool = False):
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
        # list_rpc_call, list_call_id = [], []
        for value in queries:
            key = value.id
            # fn_paras = value.f
            block_number = value.block_number
            items = key.split('_')
            if Token.native_token == items[1] and "balanceof" == items[0]:
                fn_paras = items[2]
                self.w3_multicall.add(W3Multicall.Call(
                    address=self.multicall_contract, abi=MULTICALL_V3_ABI, fn_paras=fn_paras, fn_name='balanceof', block_number=block_number))
            else:
                self.w3_multicall.add(value)

        list_call_id, list_rpc_call = [], []
        add_rpc_multicall(self.w3_multicall, list_rpc_call=list_rpc_call, list_call_id=list_call_id, batch_size=batch_size)
        try:
            responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=1)
            decoded_data = decode_multical_response(
                w3_multicall=self.w3_multicall, data_responses=responses,
                list_call_id=list_call_id, ignore_error=True, batch_size=batch_size
            )
            return decoded_data

        except Exception as e:
            logger.error(f"Error while send batch to provider: {e}")

    @staticmethod
    def add_native_token_balance_rpc_call(
            fn_paras: str = None, call_id: str = None, block_number: int = "latest"):
        eth_call = GetBalance(Web3.to_checksum_address(fn_paras), block_number, call_id)
        return eth_call

    def add_rpc_call(self, abi: dict, fn_name: str, contract_address: str,
                     fn_paras: list = None, call_id: str = None, block_number: int = "latest"):
        args = []
        if fn_paras:
            for item in fn_paras:
                if self._w3.is_address(item):
                    item = self._w3.to_checksum_address(item)
                args.append(item)

        c = contract.Contract
        c.w3 = self._w3
        c.abi = abi
        data_call = c.encodeABI(fn_name=fn_name, args=args)
        # data_call = encode_eth_call_data(abi=abi, fn_name=fn_name, args=args)
        eth_call = EthCall(to=self._w3.to_checksum_address(contract_address), block_number=block_number,
                           data=data_call, abi=abi, fn_name=fn_name, id=call_id)
        return eth_call

    def decode_response_data(self, response_data: dict, list_call_id: list, ignore_error=False):
        decoded_data = {}
        for call_id in list_call_id:
            try:
                response_datum = response_data.get(call_id)
                decoded_datum = response_datum.decode_result()
            except Exception as e:
                decoded_datum = self.check_data(call_id, response_datum)
                if decoded_datum is not None:
                    decoded_data[call_id] = decoded_datum
                    continue
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

    def create_batch_w3_provider(self):
        return ThreadLocalProxy(lambda: get_provider_from_uri(self.provider_uri, batch=True))

    @staticmethod
    def generate_json_rpc(method, params, request_id=1):
        return {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': request_id,
        }

    @staticmethod
    def check_data(call_id: str, data):
        keys = call_id.split("_")
        fn = keys[0]
        if fn == "underlying" and data.result == "0x":
            return Token.native_token
        if fn == "decimals" and keys[1] in ProtocolNFT.nft:
            return 0
        return None
