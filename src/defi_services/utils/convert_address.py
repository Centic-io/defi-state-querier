import base58
from web3 import Web3


def hex_to_base58(hex_string):
    if hex_string[:2] in ["0x", "0X"]:
        hex_string = "41" + hex_string[2:]
    bytes_str = bytes.fromhex(hex_string)
    base58_str = base58.b58encode_check(bytes_str)
    return base58_str.decode("UTF-8")


def base58_to_hex(base58_string):
    asc_string = base58.b58decode_check(base58_string)
    hex_string = asc_string.hex()
    hex_string = f"0x{hex_string[2:]}"
    return hex_string


def convert_address_dict(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if Web3.isAddress(key):
                key = hex_to_base58(key)
            if isinstance(value, dict):
                value = convert_address_dict(value)
            if Web3.isAddress(value):
                value = hex_to_base58(value)
            result[key] = value
        return result

    if isinstance(data, list):
        result = []
        for item in data:
            result.append(convert_address_dict(item))
        return result

    return data
