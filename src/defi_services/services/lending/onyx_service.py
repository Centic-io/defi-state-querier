import logging
import time

from web3 import Web3

from defi_services.abis.lending.onyx.onyx_lens_abi import ONYX_LENS_ABI
from defi_services.abis.lending.onyx.onyx_token_abi import ONYX_TOKEN_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.state_querier import StateQuerier
from defi_services.services.lending.lending_info.ethereum.onyx_eth import ONYX_ETH
from defi_services.abis.lending.onyx.onyx_comptroller_abi import ONYX_COMPTROLLER_ABI
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Onyx Lending Pool State Service")


class OnyxInfo:
    mapping = {
        Chain.ethereum: ONYX_ETH
    }


class OnyxStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        self.name = f"{chain_id}_onyx-protocol"
        self.chain_id = chain_id
        self.pool_info = OnyxInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = ONYX_LENS_ABI
        self.comptroller_abi = ONYX_COMPTROLLER_ABI
        self.token_abi = ONYX_TOKEN_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            "onyx-protocol": {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(
            self,
            block_number: int = "latest"):
        _w3 = self.state_service.get_w3()
        comptroller_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.pool_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        ctokens = []
        for token in comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number):
            if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
                         ContractAddresses.UST]:
                continue
            ctokens.append(token)

        lens_contract = _w3.eth.contract(
            address=Web3.toChecksumAddress(self.pool_info.get("lensAddress")), abi=self.lens_abi
        )
        tokens = [Web3.toChecksumAddress(i) for i in ctokens]
        metadata = lens_contract.functions.oTokenMetadataAll(tokens).call(block_identifier=block_number)
        reserves_info = {}
        for data in metadata:
            underlying = data[11].lower()
            ctoken = data[0].lower()
            lt = data[10] / 10 ** 18
            reserves_info[underlying] = {
                "cToken": ctoken,
                "liquidationThreshold": lt
            }

        return reserves_info

    def get_token_list(self):
        begin = time.time()
        tokens = [self.pool_info.get('rewardToken'), self.pool_info.get("poolToken")]
        for token in self.pool_info.get("reservesList"):
            if token == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
                continue
            tokens.append(token)
        logger.info(f"Get token list related in {time.time() - begin}s")
        return tokens

    def get_data(
            self,
            query_types: list,
            wallet: str,
            decoded_data: dict,
            block_number: int = 'latest',
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", self.pool_info.get("reservesList"))
        token_prices = kwargs.get("token_prices", {})
        pool_decimals = kwargs.get("pool_decimals", 18)
        result = {}
        if Query.deposit_borrow in query_types and wallet:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            result.update(self.calculate_rewards_balance(
                wallet, decoded_data, block_number
            ))

        logger.info(f"Process protocol data in {time.time() - begin}")
        return result

    def get_function_info(
            self,
            query_types: list,
            wallet: str = None,
            block_number: int = "latest",
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", {})
        is_oracle_price = kwargs.get("is_oracle_price", False)  # get price by oracle
        if not reserves_info:
            reserves_info = self.pool_info['reservesList']
        rpc_calls = {}
        if Query.deposit_borrow in query_types and wallet:
            rpc_calls.update(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            rpc_calls.update(self.get_rewards_balance_function_info(wallet, block_number))

        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return rpc_calls

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        token = self.pool_info.get("poolToken")
        fn_paras = [Web3.toChecksumAddress(token),
                    Web3.toChecksumAddress(self.pool_info.get("comptrollerAddress")),
                    Web3.toChecksumAddress(wallet_address)]
        rpc_call = self.get_lens_function_info("getXcnBalanceMetadataExt", fn_paras, block_number)
        get_reward_id = f"getXcnBalanceMetadataExt_{wallet_address}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(self, wallet_address: str, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"getXcnBalanceMetadataExt_{wallet_address}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id)[-1] / 10 ** 18
        reward_token = self.pool_info.get("rewardToken")
        result = {
            reward_token: {"amount": rewards}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet_address: str,
            reserves_info: dict,
            block_number: int = "latest",
    ):

        rpc_calls = {}
        ctokens = []

        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get('cToken')
            ctokens.append(Web3.toChecksumAddress(ctoken))

            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            if value.get("decimals"):
                continue
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, ERC20_ABI, "decimals", [], block_number
            )
        key = f"oTokenBalancesAll_{wallet_address}_{block_number}".lower()
        rpc_calls[key] = self.get_lens_function_info("oTokenBalancesAll", [ctokens, Web3.toChecksumAddress(wallet_address)])
        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self, wallet_address: str, reserves_info: dict, decoded_data: dict, token_prices: dict = None,
            block_number: int = "latest"):
        if token_prices is None:
            token_prices = {}
        result = {}
        key = f"oTokenBalancesAll_{wallet_address}_{block_number}".lower()
        ctoken_balance = {}
        for item in decoded_data.get(key):
            ctoken_balance[item[0]] = {
                "borrow": item[2],
                "supply": item[3]
            }
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get("cToken")
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)

            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data.get(get_decimals_id, 0)
            deposit_amount = ctoken_balance[ctoken]["supply"] / 10 ** decimals
            borrow_amount = ctoken_balance[ctoken]["borrow"] / 10 ** decimals
            result[token] = {
                "borrow_amount": borrow_amount,
                "deposit_amount": deposit_amount,
            }
            if token_prices:
                token_price = token_prices.get(underlying)
            else:
                token_price = None
            if token_price is not None:
                deposit_amount_in_usd = deposit_amount * token_price
                borrow_amount_in_usd = borrow_amount * token_price
                result[token]['borrow_amount_in_usd'] += borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] += deposit_amount_in_usd
        return result

    # TOKEN DEPOSIT BORROW BALANCE
    def get_token_deposit_borrow_balance_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            ctoken = value.get('cToken')
            underlying_borrow_key = f"totalBorrows_{ctoken}_{block_number}".lower()
            underlying_balance_key = f"totalSupply_{ctoken}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            ctoken_decimals_key = f"decimals_{ctoken}_{block_number}".lower()
            exchange_rate_key = f"exchangeRateCurrent_{ctoken}_{block_number}".lower()
            rpc_calls[underlying_borrow_key] = self.get_ctoken_function_info(
                ctoken, "totalBorrows", [], block_number)
            rpc_calls[underlying_balance_key] = self.get_ctoken_function_info(
                ctoken, "totalSupply", [], block_number)
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, ERC20_ABI, "decimals", [], block_number
            )
            rpc_calls[ctoken_decimals_key] = self.state_service.get_function_info(
                ctoken, ERC20_ABI, "decimals", [], block_number
            )
            rpc_calls[exchange_rate_key] = self.get_ctoken_function_info(
                ctoken, "exchangeRateCurrent", [], block_number)

        return rpc_calls

    def calculate_token_deposit_borrow_balance(
            self, decoded_data: dict, reserves_info: dict, token_prices: dict = None,
            block_number: int = "latest"
    ):
        result = {}
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get("cToken")
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            get_total_deposit_id = f"totalSupply_{ctoken}_{block_number}".lower()
            get_total_borrow_id = f"totalBorrows_{ctoken}_{block_number}".lower()
            get_exchange_rate = f"exchangeRateCurrent_{ctoken}_{block_number}".lower()
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            get_ctoken_decimals_id = f"decimals_{ctoken}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            ctoken_decimals = decoded_data[get_ctoken_decimals_id]
            exchange_rate = decoded_data[get_exchange_rate] / 10 ** (18 - 8 + decimals)
            deposit_amount = decoded_data[get_total_deposit_id] * exchange_rate / 10 ** ctoken_decimals
            borrow_amount = decoded_data[get_total_borrow_id] / 10 ** decimals
            result[token] = {
                "borrow_amount": borrow_amount,
                "deposit_amount": deposit_amount
            }
            if token_prices:
                token_price = token_prices.get(underlying)
            else:
                token_price = None
            if token_price is not None:
                deposit_amount_in_usd = deposit_amount * token_price
                borrow_amount_in_usd = borrow_amount * token_price
                result[token]['borrow_amount_in_usd'] += borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] += deposit_amount_in_usd
        return result

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_comptroller_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['comptrollerAddress'], self.comptroller_abi, fn_name, fn_paras, block_number
        )

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, self.token_abi, fn_name, fn_paras, block_number
        )

    def get_ctoken_metadata_all(
            self,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"cTokenMetadataAll_{self.pool_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("cTokenMetadataAll", tokens, block_number)
        }

    def ctoken_underlying_price_all(
            self, reserves_info, block_number: int = 'latest'):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"cTokenUnderlyingPriceAll_{self.pool_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("cTokenUnderlyingPriceAll", tokens, block_number)
        }

    def get_all_markets(
            self, block_number: int = 'latest'):
        key = f"getAllMarkets_{self.pool_info.get('comptrollerAddress')}_{block_number}".lower()
        return {
            key: self.get_comptroller_function_info("getAllMarkets", [], block_number)
        }
