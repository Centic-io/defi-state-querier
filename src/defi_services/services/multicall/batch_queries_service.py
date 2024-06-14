from query_state_lib.base.mappers.eth_call_mapper import EthCall
from web3 import Web3, contract

from defi_services.constants.token_constant import Token, ProtocolNFT
from defi_services.utils.logger_utils import get_logger

logger = get_logger('Batch queries')

w3 = Web3()


def add_rpc_call(abi, fn_name, contract_address, block_number=None, fn_paras=None, list_rpc_call=None,
                 list_call_id=None, call_id=None):
    args = []
    if fn_paras is not None:
        if type(fn_paras) is list:
            args = fn_paras
        else:
            if Web3.is_address(fn_paras):
                fn_paras = Web3.to_checksum_address(fn_paras)
            args = [fn_paras]

        if call_id is None:
            call_id = f"{fn_name}_{contract_address}_{fn_paras}_{block_number}".lower()
    else:
        if call_id is None:
            call_id = f"{fn_name}_{contract_address}_{block_number}".lower()

    if call_id in list_call_id:
        return

    c = contract.Contract
    c.w3 = w3
    c.abi = abi
    data_call = c.encodeABI(fn_name=fn_name, args=args)

    if block_number:
        eth_call = EthCall(to=Web3.to_checksum_address(contract_address), block_number=block_number, data=data_call,
                           abi=abi, fn_name=fn_name, id=call_id)
    else:
        eth_call = EthCall(to=Web3.to_checksum_address(contract_address), data=data_call,
                           abi=abi, fn_name=fn_name, id=call_id)

    list_rpc_call.append(eth_call)
    list_call_id.append(call_id)


def decode_data_response(data_responses, list_call_id):
    decoded_datas = {}
    for call_id in list_call_id:
        try:
            response_data = data_responses.get(call_id)
            decoded_data = response_data.decode_result()
        except Exception as e:
            logger.error(f"An exception when decode data from provider: {e}")
            raise

        if len(decoded_data) == 1:
            decoded_datas[call_id] = decoded_data[0]
        else:
            decoded_datas[call_id] = decoded_data
    return decoded_datas


def decode_data_response_ignore_error(data_responses, list_call_id):
    decoded_datas = {}
    for call_id in list_call_id:
        response_data = data_responses.get(call_id)
        try:
            decoded_data = response_data.decode_result()
        except OverflowError:
            result = response_data.result
            if result.startswith('0x'):
                result = result[2:]
            bytes_array = bytearray.fromhex(result)
            bytes32 = bytes_array.hex().rstrip("0")
            if len(bytes32) % 2 != 0:
                bytes32 = bytes32 + '0'
            decoded_data = bytes.fromhex(bytes32).decode('utf8')
        except Exception as e:
            decoded_datum = check_data(call_id, response_data)
            if decoded_datum is not None:
                decoded_datas[call_id] = decoded_datum
                continue
            logger.error(f"An exception when decode data from provider: {e}")
            continue

        if len(decoded_data) == 1:
            decoded_datas[call_id] = decoded_data[0]
        else:
            decoded_datas[call_id] = decoded_data
    return decoded_datas


def check_data(call_id: str, data):
    keys = call_id.split("_")
    fn = keys[0]
    if fn == "underlying" and data.result == "0x":
        return Token.native_token
    if fn == "decimals" and keys[1] in ProtocolNFT.nft:
        return 0
    return None
