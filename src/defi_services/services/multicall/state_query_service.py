import itertools

from query_state_lib.base.mappers.eth_call_balance_of_mapper import EthCallBalanceOf
from query_state_lib.base.mappers.get_balance_mapper import GetBalance
from query_state_lib.client.client_querier import ClientQuerier
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from defi_services.abis.dex.pancakeswap.pancakeswap_lp_token_abi import LP_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.abis.token.erc721_abi import ERC721_ABI
from defi_services.constants.network_constants import NATIVE_TOKEN
from defi_services.services.eth.eth_services import EthService
from defi_services.services.multicall.batch_queries_service import add_rpc_call, decode_data_response_ignore_error
from defi_services.utils.logger_utils import get_logger

logger = get_logger('State Query Service')


class StateQueryService:
    def __init__(self, provider_uri):
        self._w3 = Web3(HTTPProvider(provider_uri))
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.client_querier = ClientQuerier(provider_url=provider_uri)

    def get_web3(self):
        return self._w3

    def to_checksum(self, address):
        return self._w3.to_checksum_address(address)

    def get_contract(self, address, abi):
        try:
            return self._w3.eth.contract(self.to_checksum(address), abi=abi)
        except TypeError:
            print('a')

    def is_contract(self, address):
        code = self._w3.eth.get_code(self.to_checksum(address))
        code_str = code.hex()
        if code_str == '0x':
            return False
        else:
            return True

    def decode_tx(self, address, abi, tx_input):
        contract = self.get_contract(address, abi)
        func_obj, func_params = contract.decode_function_input(tx_input)
        return func_obj, func_params

    def is_address(self, address):
        return self._w3.is_address(address)

    def balance_of(self, address, token, abi=ERC20_ABI, block_number='latest'):
        token_contract = self._w3.eth.contract(self._w3.to_checksum_address(token), abi=abi)
        decimals = token_contract.functions.decimals().call()
        balance = token_contract.functions.balanceOf(self._w3.to_checksum_address(address)).call(
            block_identifier=block_number)
        return balance / 10 ** decimals

    def batch_balance_of(self, address, tokens, block_number: int = 'latest', batch_size=100):
        balances = {}
        tokens = {token['address']: token['decimals'] or 18 for token in tokens}
        rpc_requests = []
        for token in tokens:
            if token != "0x" and token != NATIVE_TOKEN:
                query_id = f'{address}_{token}'
                call_balance_of = EthCallBalanceOf(
                    contract_address=Web3.to_checksum_address(token),
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            else:
                query_id = f"{address}_{NATIVE_TOKEN}"
                call_balance_of = GetBalance(
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            rpc_requests.append(call_balance_of)
        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)
        for token, decimals in tokens.items():
            if token == '0x':
                token = NATIVE_TOKEN
            balance = rpc_responses.get(f'{address}_{token}').result or 0
            balance = balance / 10 ** decimals
            balances[token] = balance

        return balances

    def batch_balance_of_multiple_addresses(self, addresses, tokens, block_number='latest', batch_size=100):
        tokens_decimals = {token['address']: token.get('decimals') or 18 for token in tokens}

        rpc_requests = []
        for address, interacted_tokens in addresses.items():
            for token_address in interacted_tokens:
                if token_address != "0x" and token_address != NATIVE_TOKEN:
                    query_id = f'{address}_{token_address}'
                    call_balance_of = EthCallBalanceOf(
                        contract_address=Web3.to_checksum_address(token_address),
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                else:
                    query_id = f"{address}_{NATIVE_TOKEN}"
                    call_balance_of = GetBalance(
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        results = {}
        for address, interacted_tokens in addresses.items():
            results[address] = {}
            for token_address in interacted_tokens:
                balance = rpc_responses.get(f'{address}_{token_address}').result or 0

                decimals = tokens_decimals.get(token_address) or 18
                balance = balance / 10 ** decimals
                results[address][token_address] = balance

        return results, len(rpc_requests)

    def get_block_number_by_timestamp(self, block_timestamp):
        eth_service = EthService(self._w3)
        block_number = eth_service.get_block_for_timestamp(block_timestamp)
        return block_number

    def batch_native_balance_of_wallets(self, addresses, blocks, decimals=18, batch_size=100):
        rpc_requests = []
        for address in addresses:
            for block_number in blocks:
                query_id = f"{address}_{block_number}"
                call_balance_of = GetBalance(
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
                rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        data = {}
        for address in addresses:
            data[address] = {}
            for block_number in blocks:
                balance = rpc_responses.get(f'{address}_{block_number}').result or 0
                balance = balance / 10 ** decimals
                data[address][block_number] = balance

        return data

    def batch_balance_of_wallets(self, addresses, tokens, blocks, batch_size=100):
        rpc_requests = []

        for address, token, block_number in itertools.product(addresses, tokens, blocks):
            token_address = token['address']
            query_id = f'{address}_{token_address}_{block_number}'
            if token_address != "0x" and token_address != NATIVE_TOKEN:
                call_balance_of = EthCallBalanceOf(
                    contract_address=Web3.to_checksum_address(token_address),
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            else:
                call_balance_of = GetBalance(
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        data = {}
        for address, token, block_number in itertools.product(addresses, tokens, blocks):
            token_address = token['address']
            query_id = f'{address}_{token_address}_{block_number}'
            balance = rpc_responses.get(query_id).result or 0

            decimals = token.get('decimals') or 18

            if address not in data:
                data[address] = {}
            if token_address not in data[address]:
                data[address][token_address] = {}
            data[address][token_address][block_number] = balance / 10 ** decimals

        return data

    def batch_balance_of_wallets_block(self, addresses, tokens, block_number='latest', batch_size=100):
        rpc_requests = []
        for address, token in itertools.product(addresses, tokens):
            token_address = token['address']
            query_id = f'{address}_{token_address}_{block_number}'
            if token_address != "0x" and token_address != NATIVE_TOKEN:
                call_balance_of = EthCallBalanceOf(
                    contract_address=Web3.to_checksum_address(token_address),
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            else:
                call_balance_of = GetBalance(
                    address=Web3.to_checksum_address(address),
                    block_number=block_number,
                    id=query_id
                )
            rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        data = {}
        for address, token in itertools.product(addresses, tokens):
            token_address = token['address']
            query_id = f'{address}_{token_address}_{block_number}'
            balance = rpc_responses.get(query_id).result or 0
            decimals = token.get('decimals') or 18
            if address not in data:
                data[address] = {}
            if token_address not in data[address]:
                data[address][token_address] = {}
            data[address][token_address] = balance / 10 ** decimals

        return data

    def batch_balance_of_wallet_info(self, wallet_info: dict, block_number='latest', batch_size=100):
        rpc_requests = []
        for address, tokens in wallet_info.items():
            for token in tokens:
                token_address = token['address']
                query_id = f'{address}_{token_address}_{block_number}'
                if token_address != "0x" and token_address != NATIVE_TOKEN:
                    call_balance_of = EthCallBalanceOf(
                        contract_address=Web3.to_checksum_address(token_address),
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                else:
                    call_balance_of = GetBalance(
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        data = {}
        for address, tokens in wallet_info.items():
            for token in tokens:
                token_address = token['address']
                query_id = f'{address}_{token_address}_{block_number}'
                balance = rpc_responses.get(query_id).result or 0
                decimals = token.get('decimals') or 18
                if address not in data:
                    data[address] = {}
                if token_address not in data[address]:
                    data[address][token_address] = {}
                data[address][token_address] = balance / 10 ** decimals

        return data

    def batch_balance_of_wallet_info_with_block_number(self, wallets_info: list, batch_size=100):
        rpc_requests = []
        for wallet_info in wallets_info:
            address = wallet_info['address']
            tokens = wallet_info.get('tokens', [])
            block_number = wallet_info.get('block_number', 'latest')

            for token in tokens:
                token_address = token['address']
                query_id = f'{address}_{token_address}_{block_number}'
                if token_address != "0x" and token_address != NATIVE_TOKEN:
                    call_balance_of = EthCallBalanceOf(
                        contract_address=Web3.to_checksum_address(token_address),
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                else:
                    call_balance_of = GetBalance(
                        address=Web3.to_checksum_address(address),
                        block_number=block_number,
                        id=query_id
                    )
                rpc_requests.append(call_balance_of)

        rpc_responses = self.client_querier.sent_batch_to_provider(rpc_requests, batch_size=batch_size)

        data = {}
        for wallet_info in wallets_info:
            address = wallet_info['address']
            tokens = wallet_info.get('tokens', [])
            block_number = wallet_info.get('block_number', 'latest')

            for token in tokens:
                token_address = token['address']
                query_id = f'{address}_{token_address}_{block_number}'
                balance = rpc_responses.get(query_id).result or 0
                decimals = token.get('decimals')
                if decimals is None:
                    continue

                if address not in data:
                    data[address] = {}
                if token_address not in data[address]:
                    data[address][token_address] = {}
                data[address][token_address] = balance / 10 ** decimals

        return data

    def recheck_liquidity_pool_v2_reserves(self, liquidity_pools: list, batch_size=100):
        list_rpc_call = []
        list_call_id = []

        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']
            block_number = liquidity_pool.get('block_number', 'latest')

            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="getReserves", block_number=block_number,
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )

        responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=batch_size)
        decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)

        data = {}
        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']
            tokens = liquidity_pool.get('tokens', [])
            block_number = liquidity_pool.get('block_number', 'latest')

            reserves = decoded_data.get(f'getReserves_{address}_{block_number}'.lower())
            if not reserves:
                continue
            for token in tokens:
                token_address = token['address']
                balance = reserves[token['idx']]
                decimals = token.get('decimals')
                if decimals is None:
                    continue

                if address not in data:
                    data[address] = {}
                if token_address not in data[address]:
                    data[address][token_address] = {}
                data[address][token_address] = balance / 10 ** decimals

        return data

    def batch_total_supply_pool_info_with_block_number(self, liquidity_pools: list, batch_size=100):
        list_rpc_call = []
        list_call_id = []
        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']
            block_number = liquidity_pool['block_number']

            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="totalSupply", block_number=block_number,
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )
            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="decimals", block_number="latest",
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )
        try:
            responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=batch_size)
            decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)
        except Exception as ex:
            err_detail = str(ex)
            if err_detail.strip().startswith('Response data err'):
                return
            raise ex
        data = {}
        for liquidity_pool in liquidity_pools:
            try:
                address = liquidity_pool['address']
                block_number = liquidity_pool['block_number']
                total_supply = decoded_data.get(f'totalSupply_{address}_{block_number}'.lower())
                decimals = decoded_data.get(f'decimals_{address}_latest'.lower())
                data[address] = {
                    "liquidityAmount": total_supply / 10 ** decimals,
                    'decimals': decimals,
                }

            except Exception:
                continue

        return data

    def batch_nfts_info(self, addresses, batch_size=100):
        list_rpc_call = []
        list_call_id = []
        for address in addresses:
            add_rpc_call(
                abi=ERC721_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="name", block_number='latest',
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )

            add_rpc_call(
                abi=ERC721_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="symbol", block_number='latest',
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )

        responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=batch_size)
        decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)

        data = {}
        for address in addresses:
            query_name_id = f'name_{address}_latest'
            query_symbol_id = f'symbol_{address}_latest'

            name = decoded_data.get(query_name_id)
            symbol = decoded_data.get(query_symbol_id)
            if name and symbol:
                data[address] = {
                    "name": name,
                    "symbol": symbol
                }

        return data

    def batch_liquidity_pools_tokens(self, liquidity_pools, batch_size=100):
        list_rpc_call = []
        list_call_id = []
        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']

            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="token0", block_number="latest",
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )
            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="token1", block_number="latest",
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )
            add_rpc_call(
                abi=LP_TOKEN_ABI, contract_address=Web3.to_checksum_address(address),
                fn_name="factory", block_number="latest",
                list_call_id=list_call_id, list_rpc_call=list_rpc_call
            )

        try:
            responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=batch_size)
            decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)
        except Exception as ex:
            err_detail = str(ex)
            if err_detail.strip().startswith('Response data err'):
                return
            raise ex

        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']

            token0_address = decoded_data.get(f'token0_{address}_latest'.lower())
            token1_address = decoded_data.get(f'token1_{address}_latest'.lower())
            factory = decoded_data.get(f'factory_{address}_latest'.lower())

            if token0_address and token1_address:
                liquidity_pool.update({
                    "address": address,
                    "factoryAddress": factory,
                    "tokens": [
                        {
                            "idx": 0,
                            "address": token0_address.lower()
                        },
                        {
                            "idx": 1,
                            "address": token1_address.lower()
                        }
                    ]
                })

        return liquidity_pools

    def batch_liquidity_pools_info(self, liquidity_pools, batch_size=100):
        list_rpc_call = []
        list_call_id = []
        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']
            block_number = liquidity_pool['block_number']

            for token in liquidity_pool.get('tokens', []):
                add_rpc_call(
                    abi=ERC20_ABI, contract_address=Web3.to_checksum_address(token['address']),
                    fn_name="decimals", block_number='latest',
                    list_call_id=list_call_id, list_rpc_call=list_rpc_call
                )
                add_rpc_call(
                    abi=ERC20_ABI, contract_address=Web3.to_checksum_address(token['address']),
                    fn_name="symbol", block_number='latest',
                    list_call_id=list_call_id, list_rpc_call=list_rpc_call
                )
                add_rpc_call(
                    abi=ERC20_ABI, contract_address=Web3.to_checksum_address(token['address']),
                    fn_name="balanceOf", fn_paras=address, block_number=block_number,
                    list_call_id=list_call_id, list_rpc_call=list_rpc_call
                )

        try:
            responses = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=batch_size)
            decoded_data = decode_data_response_ignore_error(data_responses=responses, list_call_id=list_call_id)
        except Exception as ex:
            err_detail = str(ex)
            if err_detail.strip().startswith('Response data err'):
                return
            raise ex

        for liquidity_pool in liquidity_pools:
            address = liquidity_pool['address']
            block_number = liquidity_pool['block_number']

            try:
                for token in liquidity_pool.get('tokens', []):
                    symbol = decoded_data.get(f'symbol_{token["address"]}_latest'.lower())
                    symbol = symbol.upper() if symbol else ""
                    decimals = decoded_data.get(f'decimals_{token["address"]}_latest'.lower())

                    liquidity_amount = decoded_data.get(f'balanceOf_{token["address"]}_{address}_{block_number}'.lower(), 0)
                    token['liquidityAmount'] = liquidity_amount / 10 ** decimals
                    token['symbol'] = symbol
                    token['decimals'] = decimals

                liquidity_pool['symbol'] = ' - '.join([t['symbol'] for t in liquidity_pool.get('tokens', [])])
            except Exception as ex:
                logger.exception(ex)

                # Add to invalid liquidity pools
                liquidity_pool.pop('tokens')

        return liquidity_pools
