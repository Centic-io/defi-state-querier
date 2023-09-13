import logging
import time

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.iron_bank.iron_lens_abi import IRON_LENS_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.avalanche.iron_bank_avalanche import IRON_BANK_AVALANCHE
from defi_services.services.lending.lending_info.ethereum.iron_bank_eth import IRON_BANK_ETH
from defi_services.services.lending.lending_info.optimism.iron_bank_optimism import IRON_BANK_OPTIMISM
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Iron Bank Lending Pool State Service")


class IronBankInfo:
    mapping = {
        Chain.ethereum: IRON_BANK_ETH,
        Chain.optimism: IRON_BANK_OPTIMISM,
        Chain.avalanche: IRON_BANK_AVALANCHE
    }


class IronBankStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        self.name = f"{chain_id}_{Lending.iron_bank}"
        self.chain_id = chain_id
        self.iron_bank_info = IronBankInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = IRON_LENS_ABI
        self.comptroller_abi = CREAM_COMPTROLLER_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.iron_bank: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.iron_bank_info
            }
        }
        return info

    def get_dapp_asset_info(
            self,
            block_number: int = "latest"):
        _w3 = self.state_service.get_w3()
        comptroller_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.iron_bank_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        ctokens = []
        for token in comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number):
            if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
                         ContractAddresses.UST]:
                continue
            ctokens.append(token)

        lens_contract = _w3.eth.contract(
            address=Web3.toChecksumAddress(self.iron_bank_info.get("lensAddress")), abi=self.lens_abi
        )
        tokens = [Web3.toChecksumAddress(i) for i in ctokens]
        metadata = lens_contract.functions.cTokenMetadataAll(tokens).call(block_identifier=block_number)

        reserves_info = {}
        for data in metadata:
            underlying = data[12].lower()
            ctoken = data[0].lower()
            lt = data[11] / 10 ** 18
            reserves_info[underlying] = {
                "cToken": ctoken,
                "liquidationThreshold": lt
            }

        return reserves_info

    def get_token_list(self):
        begin = time.time()
        tokens = [self.iron_bank_info.get('rewardToken'), self.iron_bank_info.get("poolToken")]
        for token in self.iron_bank_info.get("reservesList"):
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
        reserves_info = kwargs.get("reserves_info", self.iron_bank_info.get("reservesList"))
        token_prices = kwargs.get("token_prices", {})
        wrapped_native_token_price = token_prices.get(Token.wrapped_token.get(self.chain_id), 1)
        pool_decimals = kwargs.get("pool_decimals", 18)
        result = {}
        if Query.deposit_borrow in query_types and wallet:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, wrapped_native_token_price, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            result.update(self.calculate_claimable_rewards_balance(
                wallet, decoded_data, block_number
            ))

        # if Query.protocol_apy in query_types and wallet:
        #     result.update(self.calculate_apy_lending_pool_function_call(
        #         reserves_info, decoded_data, token_prices, pool_decimals, block_number
        #     ))
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
            reserves_info = self.iron_bank_info['reservesList']
        rpc_calls = {}
        if Query.deposit_borrow in query_types and wallet:
            rpc_calls.update(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number, is_oracle_price
            ))

        # if Query.protocol_apy in query_types:
        #     rpc_calls.update(self.get_apy_lending_pool_function_info(reserves_info, block_number, is_oracle_price))

        if Query.protocol_reward in query_types and wallet:
            rpc_calls.update(self.get_claimable_rewards_balance_function_info(wallet, block_number))

        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return rpc_calls

    # REWARDS BALANCE
    def get_claimable_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        rpc_call = self.get_comptroller_function_info("compAccrued", [wallet_address], block_number)
        get_reward_id = f"compAccrued_{self.name}_{wallet_address}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_claimable_rewards_balance(
            self, wallet_address: str, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"compAccrued_{self.name}_{wallet_address}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id) / 10 ** 18
        reward_token = self.iron_bank_info.get("rewardToken")
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
            is_oracle_price: bool = False
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get('cToken')
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            underlying_price_key = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
            underlying_borrow_key = f"borrowBalanceCurrent_{ctoken}_{wallet_address}_{block_number}".lower()
            underlying_balance_key = f"balanceOfUnderlying_{ctoken}_{wallet_address}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            if is_oracle_price:
                rpc_calls[underlying_price_key] = self.get_lens_function_info(
                    "cTokenUnderlyingPrice", [ctoken], block_number)
            rpc_calls[underlying_borrow_key] = self.get_ctoken_function_info(
                ctoken, "borrowBalanceCurrent", [wallet_address], block_number)
            rpc_calls[underlying_balance_key] = self.get_ctoken_function_info(
                ctoken, "balanceOfUnderlying", [wallet_address], block_number)
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, ERC20_ABI, "decimals", [], block_number
            )

        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self, wallet_address: str, reserves_info: dict, decoded_data: dict, token_prices: dict = None,
            wrapped_native_token_price: int = 310, block_number: int = "latest", is_oracle_price: bool = False):
        if token_prices is None:
            token_prices = {}
        result = {}
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get("cToken")
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            get_total_deposit_id = f"balanceOfUnderlying_{ctoken}_{wallet_address}_{block_number}".lower()
            get_total_borrow_id = f"borrowBalanceCurrent_{ctoken}_{wallet_address}_{block_number}".lower()
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            deposit_amount = decoded_data[get_total_deposit_id] / 10 ** decimals
            borrow_amount = decoded_data[get_total_borrow_id] / 10 ** decimals
            result[token] = {
                "borrow_amount": borrow_amount,
                "deposit_amount": deposit_amount,
            }
            if is_oracle_price:
                get_underlying_token_price = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
                token_price = decoded_data.get(get_underlying_token_price)[
                                  1] * wrapped_native_token_price / 10 ** decimals
            elif token_prices:
                token_price = token_prices.get(underlying)
            else:
                token_price = None
            if token_price is not None:
                deposit_amount_in_usd = deposit_amount * token_price
                borrow_amount_in_usd = borrow_amount * token_price
                result[token]['borrow_amount_in_usd'] = borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] = deposit_amount_in_usd
        return result

    # TOKEN DEPOSIT BORROW BALANCE
    def get_token_deposit_borrow_balance_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
            is_oracle_price: bool = False
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            ctoken = value.get('cToken')
            underlying_price_key = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
            underlying_borrow_key = f"totalBorrows_{ctoken}_{block_number}".lower()
            underlying_balance_key = f"totalSupply_{ctoken}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            ctoken_decimals_key = f"decimals_{ctoken}_{block_number}".lower()
            exchange_rate_key = f"exchangeRateCurrent_{ctoken}_{block_number}".lower()
            if is_oracle_price:
                rpc_calls[underlying_price_key] = self.get_lens_function_info(
                    "cTokenUnderlyingPrice", [ctoken], block_number)
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
            block_number: int = "latest", is_oracle_price: bool = False, wrapped_native_token_price: int = 310
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
            if is_oracle_price:
                get_underlying_token_price = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
                token_price = decoded_data.get(get_underlying_token_price)[1] / 10 ** (36 - decimals)
                if wrapped_native_token_price:
                    token_price *= wrapped_native_token_price
            elif token_prices:
                token_price = token_prices.get(underlying)
            else:
                token_price = None
            if token_price is not None:
                deposit_amount_in_usd = deposit_amount * token_price
                borrow_amount_in_usd = borrow_amount * token_price
                result[token]['borrow_amount_in_usd'] = borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] = deposit_amount_in_usd
        return result


    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.iron_bank_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_comptroller_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.iron_bank_info['comptrollerAddress'], self.comptroller_abi, fn_name, fn_paras, block_number
        )

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, CTOKEN_ABI, fn_name, fn_paras, block_number
        )

    def get_ctoken_metadata_all(
            self,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"cTokenMetadataAll_{self.iron_bank_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("cTokenMetadataAll", tokens, block_number)
        }

    def ctoken_underlying_price_all(
            self, reserves_info, block_number: int = 'latest'):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"cTokenUnderlyingPriceAll_{self.iron_bank_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("cTokenUnderlyingPriceAll", tokens, block_number)
        }

    def get_all_markets(
            self, block_number: int = 'latest'):
        key = f"getAllMarkets_{self.iron_bank_info.get('comptrollerAddress')}_{block_number}".lower()
        return {
            key: self.get_comptroller_function_info("getAllMarkets", [], block_number)
        }