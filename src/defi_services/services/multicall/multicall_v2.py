from collections import defaultdict
from typing import Tuple, List, Union, Any, Optional, Dict

from query_state_lib.base.utils.decoder import decode_eth_call_data
from web3 import Web3, contract

from defi_services.abis.multicall_v3_abi import MULTICALL_V3_ABI
from defi_services.services.multicall.batch_queries_service import add_rpc_call, decode_data_response, \
    decode_data_response_ignore_error
from defi_services.utils.dict_utils import all_equal
from defi_services.utils.logger_utils import get_logger

logger = get_logger('Multicall V2')

w3 = Web3()


def get_fn_abi(abi, fn_name):
    for abi_ in abi:
        if abi_.get('type') == 'function' and abi_.get('name') == fn_name:
            return abi_

    return None


def _unpack_aggregate_outputs(outputs: Any) -> Tuple[Tuple[Union[None, bool], bytes], ...]:
    return tuple((success, output) for success, output in outputs)


class W3Multicall:
    """
    Interface for multicall3.sol contract
    """

    class Call:

        def __init__(self, address, abi, fn_name, fn_paras=None, block_number: Union[int, str] = 'latest', key=None):
            if key:
                self.id = key
            elif fn_paras is not None:
                self.id = f"{fn_name}_{address}_{fn_paras}_{block_number}".lower()
            else:
                self.id = f"{fn_name}_{address}_{block_number}".lower()

            self.address = Web3.to_checksum_address(address)
            self.fn_name = fn_name
            self.fn_abi = get_fn_abi(abi=abi, fn_name=fn_name)
            self.block_number = block_number

            args = []
            if fn_paras is not None:
                if type(fn_paras) is list:
                    for item in fn_paras:
                        if Web3.is_address(item):
                            args.append(Web3.to_checksum_address(item))
                        else:
                            args.append(item)
                else:
                    if Web3.is_address(fn_paras):
                        fn_paras = Web3.to_checksum_address(fn_paras)
                    args = [fn_paras]

            c = contract.Contract
            c.w3 = w3
            c.abi = abi

            self.data = c.encodeABI(fn_name=fn_name, args=args)

    def __init__(self, web3, address='0xcA11bde05977b3631167028862bE2a173976CA11', calls: Dict[str, 'W3Multicall.Call'] = None, require_success: bool = False):
        """
        :param web3: Web3 instance
        :param address: (optional) address of the multicall3.sol contract
        :param calls: (optional) list of W3Multicall.Call to perform
        """
        self.web3 = web3
        self.address = address
        self.calls: Dict[str, 'W3Multicall.Call'] = {} if calls is None else calls.copy()

        self.require_success = require_success

    def add(self, call: 'W3Multicall.Call'):
        self.calls[call.id] = call

    def get_params(self, calls: Optional[Dict[str, Call]] = None) -> List[Union[bool, List[List[Any]]]]:
        args = self._get_args(calls=calls)
        return args

    def decode(self, aggregated, calls: Optional[Dict[str, Call]] = None, ignore_error=True):
        if calls is None:
            calls = self.calls

        unpacked = _unpack_aggregate_outputs(aggregated)

        outputs = {}
        for (call_id, call), (success, output) in zip(calls.items(), unpacked):
            if not success:
                logger.warning(f'Fail to query {call_id}')
                continue

            try:
                call_output = '0x' + output.hex()
                decoded_data = decode_eth_call_data([call.fn_abi], call.fn_name, call_output)
            except OverflowError:
                bytes_array = bytearray.fromhex(output.hex())
                bytes32 = '0x' + bytes_array.hex().rstrip("0")
                if len(bytes32) % 2 != 0:
                    bytes32 += '0'
                decoded_data = decode_eth_call_data([call.fn_abi], call.fn_name, bytes32)
            except Exception as ex:
                logger.error(f"An exception when decode data from provider: {ex}")
                if ignore_error:
                    continue

                raise ex

            if len(decoded_data) == 1:
                decoded_data = decoded_data[0]

            outputs[call_id] = decoded_data

        return outputs

    def _get_args(self, calls: Optional[Dict[str, Call]] = None) -> List[Union[bool, List[List[Any]]]]:
        if calls is None:
            calls = self.calls

        block_numbers = [call.block_number for call in calls.values()]
        if not all_equal(block_numbers):
            raise ValueError('All calls must be queried at the same block number')

        return [self.require_success, [[call.address, call.data] for call in calls.values()]]

    def batch_calls_iterator(self, batch_size=2000):
        calls_by_block_number = defaultdict(lambda: {})
        for call_id, call in self.calls.items():
            block_number = call.block_number
            calls_by_block_number[block_number][call_id] = call

        for block_number, calls in calls_by_block_number.items():
            batch = {}

            for call_id, call in calls.items():
                batch[call_id] = call
                if len(batch) >= batch_size:
                    yield block_number, batch
                    batch = {}

            if len(batch) > 0:
                yield block_number, batch


def add_rpc_multicall(w3_multicall: W3Multicall, list_rpc_call=None, list_call_id=None, batch_size=2000):
    batch_idx = 0
    for block_number, batch_calls in w3_multicall.batch_calls_iterator(batch_size=batch_size):
        inputs = w3_multicall.get_params(calls=batch_calls)
        add_rpc_call(
            fn_name="tryAggregate", fn_paras=inputs, block_number=block_number,
            abi=MULTICALL_V3_ABI, contract_address=w3_multicall.address,
            list_call_id=list_call_id, list_rpc_call=list_rpc_call, call_id=f'{batch_idx}_{block_number}'
        )
        batch_idx += 1


def decode_multical_response(w3_multicall: W3Multicall, data_responses, list_call_id, ignore_error=True, batch_size=2000):
    if ignore_error:
        decoded_data = decode_data_response_ignore_error(data_responses=data_responses, list_call_id=list_call_id)
    else:
        decoded_data = decode_data_response(data_responses=data_responses, list_call_id=list_call_id)

    batch_idx = 0
    results = {}
    for block_number, batch_calls in w3_multicall.batch_calls_iterator(batch_size=batch_size):
        multicall_data = decoded_data.get(f'{batch_idx}_{block_number}')
        decode_multicall_data = w3_multicall.decode(multicall_data, calls=batch_calls, ignore_error=ignore_error)
        results.update(decode_multicall_data)

        batch_idx += 1

    return results
