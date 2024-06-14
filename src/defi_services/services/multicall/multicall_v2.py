import csv
import json
import time
from collections import defaultdict
from typing import Tuple, List, Union, Any, Optional, Dict

from query_state_lib.base.utils.decoder import decode_eth_call_data
from query_state_lib.client.client_querier import ClientQuerier
from web3 import Web3, contract

from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.multicall_v3_abi import MULTICALL_V3_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.network_constants import MulticallContract, Chains, Networks
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
                    args = fn_paras
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


def _test_multicall(_w3: Web3, multicall_contract, wallets, tokens):
    start_time = time.time()
    encode_time = 0

    rpc_call_id = {}

    n_calls = 0
    data = {}
    for wallet in wallets:
        start_encode_time = time.time()
        data[wallet] = {}

        w3_multicall = W3Multicall(_w3, address=MulticallContract.get_multicall_contract(Chains.arbitrum))
        for token in tokens:
            # if token['address'] == '0x0000000000000000000000000000000000000000':
            #     continue

            w3_multicall.add(W3Multicall.Call(
                Web3.to_checksum_address(token['address']),  # contract address
                ERC20_ABI,  # method signature to call
                'balanceOf',
                wallet
            ))

            decimals_call = W3Multicall.Call(
                Web3.to_checksum_address(token['address']),  # contract address
                ERC20_ABI,  # method signature to call
                'decimals'
            )
            if decimals_call not in rpc_call_id:
                w3_multicall.add(decimals_call)
                rpc_call_id[decimals_call] = None

        encode_time += time.time() - start_encode_time
        n_calls += len(w3_multicall.calls)

        # For single call
        inputs = w3_multicall.get_params()
        response = multicall_contract.functions.tryAggregate(*inputs).call()
        results = w3_multicall.decode(response)

        for token in tokens:
            # if token['address'] == '0x0000000000000000000000000000000000000000':
            #     continue

            decimals_call_id = f'decimals_{token["address"]}_latest'.lower()
            balance_call_id = f'balanceOf_{token["address"]}_{wallet}_latest'.lower()

            decimals = results.get(decimals_call_id)
            if decimals is None:
                decimals = rpc_call_id.get(decimals_call_id) or 18
            else:
                rpc_call_id[decimals_call_id] = decimals

            balance = results.get(balance_call_id)
            if balance is None:
                balance = rpc_call_id.get(balance_call_id) or 0
            else:
                rpc_call_id[balance_call_id] = balance
            balance /= 10 ** decimals

            data[wallet][token['address']] = {
                'name': token['name'],
                'symbol': token['symbol'],
                'balance': balance,
                'decimals': decimals
            }

    with open('results_multicall.json', 'w') as f:
        json.dump(data, f, indent=2)
    duration = time.time() - start_time

    print(f'There are {n_calls} calls')
    print(f'Encode took {round(encode_time, 3)}s')
    print(f'Done after {round(duration, 3)}s')

    return duration, encode_time, n_calls


def _test_state_querier(client_querier: ClientQuerier, wallets, tokens):
    start_time = time.time()

    list_call_id = []
    list_rpc_call = []

    for wallet in wallets:
        for token in tokens:
            if token['address'] == '0x0000000000000000000000000000000000000000':
                continue

            add_rpc_call(
                abi=ERC20_ABI, contract_address=Web3.to_checksum_address(token['address']),
                fn_name="balanceOf", fn_paras=wallet, block_number='latest',
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )
            add_rpc_call(
                abi=ERC20_ABI, contract_address=Web3.to_checksum_address(token['address']),
                fn_name="decimals", block_number='latest',
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )

    encode_time = time.time() - start_time
    print(f'There are {len(list_rpc_call)} calls')
    print(f'Encode took {round(encode_time, 3)}s')

    responses = client_querier.sent_batch_to_provider(list_rpc_call, batch_size=2000)
    decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)

    data = {}
    for wallet in wallets:
        data[wallet] = {}
        for token in tokens:
            if token['address'] == '0x0000000000000000000000000000000000000000':
                continue

            decimals = decoded_data.get(f'decimals_{token["address"]}_latest'.lower())
            balance = decoded_data.get(f'balanceOf_{token["address"]}_{wallet}_latest'.lower()) / 10 ** decimals

            data[wallet][token['address']] = {
                'name': token['name'],
                'symbol': token['symbol'],
                'balance': balance,
                'decimals': decimals
            }

    with open('results_querier.json', 'w') as f:
        json.dump(data, f, indent=2)
    duration = time.time() - start_time
    print(f'Done after {round(duration, 3)}s')

    return duration, encode_time, len(list_rpc_call)


def _test_multicall_with_multiprocessing(_w3: Web3, client_querier: ClientQuerier, wallets, tokens):
    start_time = time.time()

    w3_multicall = W3Multicall(_w3, address=MulticallContract.get_multicall_contract(Chains.arbitrum))
    for wallet in wallets:
        for token in tokens:
            # if token['address'] == '0x0000000000000000000000000000000000000000':
            #     continue

            w3_multicall.add(W3Multicall.Call(
                Web3.to_checksum_address(token['address']),  # contract address
                ERC20_ABI,  # method signature to call
                'balanceOf',
                wallet
            ))

            w3_multicall.add(W3Multicall.Call(
                Web3.to_checksum_address(token['address']),  # contract address
                ERC20_ABI,  # method signature to call
                'decimals'
            ))

            w3_multicall.add(W3Multicall.Call(
                Web3.to_checksum_address(token['address']),  # contract address
                LP_TOKEN_ABI,  # method signature to call
                'token0'
            ))

    list_call_id, list_rpc_call = [], []
    add_rpc_multicall(w3_multicall, list_rpc_call=list_rpc_call, list_call_id=list_call_id)

    encode_time = time.time() - start_time

    responses = client_querier.sent_batch_to_provider(list_rpc_call, batch_size=1)
    decoded_data = decode_multical_response(
        w3_multicall=w3_multicall, data_responses=responses,
        list_call_id=list_call_id, ignore_error=True
    )

    data = {}
    for wallet in wallets:
        data[wallet] = {}
        for token in tokens:
            # if token['address'] == '0x0000000000000000000000000000000000000000':
            #     continue

            decimals_call_id = f'decimals_{token["address"]}_latest'.lower()
            balance_call_id = f'balanceOf_{token["address"]}_{wallet}_latest'.lower()

            decimals = decoded_data.get(decimals_call_id) or 18
            balance = decoded_data.get(balance_call_id, 0) / 10 ** decimals

            data[wallet][token['address']] = {
                'name': token['name'],
                'symbol': token['symbol'],
                'balance': balance,
                'decimals': decimals
            }

    with open('results_multicall_with_multiprocessing.json', 'w') as f:
        json.dump(data, f, indent=2)
    duration = time.time() - start_time

    print(f'There are {len(w3_multicall.calls)} calls')
    print(f'Encode took {round(encode_time, 3)}s')
    print(f'Done after {round(duration, 3)}s')

    return duration, encode_time, len(w3_multicall.calls)


def query_multi_contracts(n_times=20, wallets_batch_size=5, wallets_distribute_similar=True):
    with open('../../../.data/wallets.json') as f:
        wallets = json.load(f)
    wallets = ['0x6FfA563915CB3186b9Dd206D0E08bdeDcd2EA2ED']

    with open('../../../.data/tokens.json') as f:
        tokens_ = json.load(f)
    tokens_ = [
        {
            "address": "0xE2035f04040A135c4dA2f96AcA742143c57c79F9",
            "name": "UXUY",
            "symbol": "uxuy"
        },
        {
            "address": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
            "name": "Tether",
            "symbol": "usdt"
        },
        {
            "address": "0x0000000000000000000000000000000000000000",
            "name": "ETH",
            "symbol": "ETH"
        }
    ]

    print(f'There are maximum {len(wallets)} wallets')
    print(f'There are {len(tokens_)} tokens')

    if wallets_distribute_similar:
        wallets_batch = [wallets[:300], wallets[:300], wallets[:300]]
    else:
        wallets_batch = [wallets[:300], wallets[300:600], wallets[600:900]]

    # Methodology 1: Query State Lib
    start_time = time.time()
    client_querier = ClientQuerier(provider_url=Networks.providers['arbitrum'])
    starting_time_1 = time.time() - start_time
    logger.info(f'Starting state querier: {round(starting_time_1, 3)}s')

    _multiple(
        n_times=n_times, starting_time=starting_time_1, filename='query_state_lib',
        wallets=wallets_batch[0], wallets_batch_size=wallets_batch_size, tokens=tokens_, func=_test_state_querier,
        client_querier=client_querier
    )

    # Methodology 2: Multicall
    start_time = time.time()
    _w3 = Web3(Web3.HTTPProvider(Networks.providers['arbitrum']))
    starting_time_2_1 = time.time() - start_time
    multicall_address = MulticallContract.get_multicall_contract(Chains.arbitrum)
    multicall_contract = _w3.eth.contract(Web3.to_checksum_address(multicall_address), abi=MULTICALL_V3_ABI)
    starting_time_2 = time.time() - start_time
    logger.info(f'Starting multicall: {round(starting_time_2, 3)}s')

    _multiple(
        n_times=n_times, starting_time=starting_time_2, filename='multicall',
        wallets=wallets_batch[1], wallets_batch_size=wallets_batch_size, tokens=tokens_, func=_test_multicall,
        _w3=_w3, multicall_contract=multicall_contract
    )

    # Methodology 3: Combine Multicall with multiprocessing
    starting_time_3 = starting_time_1 + starting_time_2_1
    logger.info(f'Starting combined: {round(starting_time_3, 3)}s')

    _multiple(
        n_times=n_times, starting_time=starting_time_3, filename='combined',
        wallets=wallets_batch[2], wallets_batch_size=wallets_batch_size, tokens=tokens_,
        func=_test_multicall_with_multiprocessing, _w3=_w3, client_querier=client_querier
    )


def _multiple(n_times, starting_time, filename, wallets, wallets_batch_size, tokens, func, *args, **kwargs):
    data = [['Total Time', 'Encode Time']]
    overview = {
        'avg_total_time': 0, 'avg_encode_time': 0,
        'times': 0, 'errors': 0,
        'queries': 0, 'start_time': starting_time
    }
    for i in range(n_times):
        idx = i * wallets_batch_size
        sub_wallets = wallets[idx:idx + wallets_batch_size]
        try:
            total_time, encode_time, n_calls = func(wallets=sub_wallets, tokens=tokens, *args, **kwargs)

            overview['queries'] = n_calls
            data.append([total_time, encode_time])
            overview['times'] += 1
        except Exception as ex:
            logger.exception(ex)
            overview['errors'] += 1
        finally:
            time.sleep(13)

    with open(f'results_{filename}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    overview['avg_total_time'] = sum([t[0] for t in data[1:]]) / overview['times']
    overview['avg_encode_time'] = sum([t[1] for t in data[1:]]) / overview['times']
    with open(f'overview_results_{filename}.json', 'w') as f:
        json.dump(overview, f, indent=2)


if __name__ == '__main__':
    query_multi_contracts(n_times=1, wallets_batch_size=1, wallets_distribute_similar=True)
