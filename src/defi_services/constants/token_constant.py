from defi_services.constants.chain_constant import Chain


class Token:
    native_token = '0x0000000000000000000000000000000000000000'
    wrapped_ethereum = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    wrapped_token = {
        Chain.ethereum: wrapped_ethereum
    }