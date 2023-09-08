import logging
import time

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.lending.wepiggy.wepiggy_distribution_abi import WEPIGGY_DISTRIBUTION_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.ethereum.wepiggy_eth import WEPIGGY_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Compound Lending Pool State Service")


class WepiggyInfo:
    mapping = {
        Chain.ethereum: WEPIGGY_ETH
    }


class WepiggyStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        self.name = f"{chain_id}_{Lending.wepiggy}"
        self.chain_id = chain_id
        self.pool_info = WepiggyInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = CREAM_LENS_ABI
        self.distribution_abi = WEPIGGY_DISTRIBUTION_ABI
        self.comptroller_abi = CREAM_COMPTROLLER_ABI

    def get_service_info(self):
        info = {
            Lending.wepiggy: {
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
        metadata = lens_contract.functions.cTokenMetadataAll(tokens).call(block_identifier=block_number)
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
        wrapped_native_token_price = token_prices.get(Token.wrapped_token.get(self.chain_id), 1)
        pool_decimals = kwargs.get("pool_decimals", 18)
        result = {}
        if Query.deposit_borrow in query_types and wallet:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, wrapped_native_token_price, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            result.update(self.calculate_rewards_balance(
                wallet, decoded_data, block_number
            ))

        if Query.protocol_apy in query_types and wallet:
            result.update(self.calculate_apy_lending_pool_function_call(
                reserves_info, decoded_data, token_prices, pool_decimals, block_number
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
                wallet, reserves_info, block_number, is_oracle_price
            ))

        if Query.protocol_apy in query_types:
            rpc_calls.update(self.get_apy_lending_pool_function_info(reserves_info, block_number, is_oracle_price))

        if Query.protocol_reward in query_types and wallet:
            rpc_calls.update(self.get_rewards_balance_function_info(wallet, block_number))

        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return rpc_calls

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
            is_price_oracle: bool = False
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            ctoken = value.get("ctoken")
            speed_key = f"compSpeeds_{ctoken}_{block_number}".lower()
            mint_key = f"mintGuardianPaused_{ctoken}_{block_number}".lower()
            borrow_key = f"borrowGuardianPaused_{token}_{block_number}".lower()
            metadata_key = f"cTokenMetadata_{ctoken}_{block_number}".lower()
            if is_price_oracle:
                price_key = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
                rpc_calls[price_key] = self.get_comptroller_function_info('cTokenUnderlyingPrice', [ctoken],
                                                                          block_number)
            rpc_calls[speed_key] = self.get_comptroller_function_info('compSpeeds', [ctoken], block_number)
            rpc_calls[mint_key] = self.get_comptroller_function_info('mintGuardianPaused', [ctoken], block_number)
            rpc_calls[borrow_key] = self.get_comptroller_function_info('borrowGuardianPaused', [ctoken], block_number)
            rpc_calls[metadata_key] = self.get_comptroller_function_info('cTokenMetadata', [ctoken], block_number)

        return rpc_calls

    @staticmethod
    def get_apy_lending_pool(
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest",
            wrapped_native_token_price: float = 310,
            underlying_price: dict = None,
            is_oracle_price: bool = False
    ):
        underlying_prices, underlying_decimals, reserve_tokens_info = {}, {}, []
        ctoken_speeds, borrow_paused_tokens, mint_paused_tokens = {}, {}, {}
        for token, value in reserves_info.items():
            ctoken = value.get('cToken')
            speeds_call_id = f'compSpeeds_{ctoken}_{block_number}'.lower()
            borrow_guardian_paused_call_id = f'borrowGuardianPaused_{ctoken}_{block_number}'.lower()
            mint_guardian_paused_call_id = f'mintGuardianPaused_{ctoken}_{block_number}'.lower()
            ctoken_speeds[ctoken] = decoded_data.get(speeds_call_id)
            borrow_paused_tokens[ctoken] = decoded_data.get(borrow_guardian_paused_call_id)
            mint_paused_tokens[ctoken] = decoded_data.get(mint_guardian_paused_call_id)
            metadata_id = f"cTokenMetadata_{ctoken}_{block_number}".lower()
            reserve_tokens_info.append(decoded_data.get(metadata_id))
            if is_oracle_price:
                underlying_id = f"cTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
                price_token = decoded_data.get(underlying_id)
                price_token = price_token[1] * wrapped_native_token_price
            else:
                price_token = underlying_price.get(token)

            underlying_decimals[ctoken] = decoded_data.get(metadata_id)[-1]
            underlying_prices[ctoken] = price_token
        return {
            "reserve_tokens_info": reserve_tokens_info,
            "ctoken_speeds": ctoken_speeds,
            "borrow_paused_tokens": borrow_paused_tokens,
            "mint_paused_tokens": mint_paused_tokens,
            "underlying_prices": underlying_prices,
            "underlying_decimals": underlying_decimals
        }

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_decimals: int = 18,
            block_number: int = "latest",
            is_oracle_price: bool = False,
    ):
        wrapped_native_token_price = token_prices.get(Token.wrapped_token.get(self.chain_id))
        pool_token_price = token_prices.get(self.pool_info.get("poolToken"))
        tokens_interest_rates = dict()
        decode_data = self.get_apy_lending_pool(
            decoded_data, reserves_info, block_number,
            wrapped_native_token_price, token_prices, is_oracle_price)

        mint_paused_tokens = decode_data["mint_paused_tokens"]
        borrow_paused_tokens = decode_data["borrow_paused_tokens"]
        reserve_tokens_info = decode_data["reserve_tokens_info"]
        ctoken_speeds = decode_data["ctoken_speeds"]
        for data in reserve_tokens_info:
            address = data[0].lower()
            underlying_token_price = float(decode_data["underlying_prices"][address])
            if is_oracle_price:
                underlying_token_price = underlying_token_price / 10 ** int(data[13])

            token_info = {
                "token": address,
                "token_decimals": data[12],
                "borrow_rate": data[3],
                "supply_rate": data[2],
                "supply": data[7],
                "borrow": data[5],
                "exchange_rate": data[1],
                "underlying": data[11].lower(),
                "underlying_price": underlying_token_price,
                "underlying_decimals": data[13],
                "speed": ctoken_speeds[address]
            }
            underlying_token = token_info['underlying']
            token_info["mint_paused"] = mint_paused_tokens[address]
            token_info["borrow_paused"] = borrow_paused_tokens[address]
            tokens_interest_rates[underlying_token] = self._calculate_interest_rates(
                token_info, pool_decimals, pool_token_price)

        return tokens_interest_rates

    @staticmethod
    def _calculate_interest_rates(token_info: dict, pool_decimals: int, pool_price: float,
                                  is_oracle_price: bool = False):
        apx_block_speed_in_seconds = 3
        exchange_rate = float(token_info["exchange_rate"]) / 10 ** (18 - 8 + token_info["underlying_decimals"])
        block_per_day = int(60 * 60 * 24 / apx_block_speed_in_seconds)
        venus_per_day = token_info["speed"] * block_per_day / 10 ** pool_decimals
        underlying_price = float(token_info["underlying_price"])
        if is_oracle_price:
            underlying_price /= 10 ** (36 - int(token_info["underlying_decimals"]))
        total_borrow = float(token_info["borrow"]) / 10 ** int(token_info["underlying_decimals"])
        total_supply = float(token_info["supply"]) * exchange_rate / 10 ** int(token_info["underlying_decimals"])
        total_borrow_usd = total_borrow * underlying_price
        total_supply_usd = total_supply * underlying_price

        if total_borrow_usd == 0:
            borrow_apr = 0
        else:
            borrow_apr = (1 + (pool_price * venus_per_day / total_borrow_usd)) ** 365 - 1

        if total_supply_usd == 0:
            supply_apr = 0
        else:
            supply_apr = (1 + (pool_price * venus_per_day / total_supply_usd)) ** 365 - 1

        supply_apy = ((token_info["supply_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1
        borrow_apy = ((token_info["borrow_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1

        liquidity_log = {
            DBConst.total_borrow: {
                DBConst.amount: total_borrow,
                DBConst.value_in_usd: total_borrow_usd
            },
            DBConst.total_deposit: {
                DBConst.amount: total_supply,
                DBConst.value_in_usd: total_supply_usd
            }
        }
        return {
            DBConst.reward_borrow_apy: borrow_apr,
            DBConst.reward_deposit_apy: supply_apr,
            DBConst.deposit_apy: supply_apy,
            DBConst.borrow_apy: borrow_apy,
            DBConst.liquidity_change_logs: liquidity_log,
            DBConst.mint_paused: token_info[DBConst.mint_paused],
            DBConst.borrow_paused: token_info[DBConst.borrow_paused]
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        token = self.pool_info.get("poolToken")
        fn_paras = [Web3.toChecksumAddress(wallet_address),
                    False,
                    True]
        rpc_call = self.get_distribution_function_info("pendingWpcAccrued", fn_paras, block_number)
        get_reward_id = f"pendingWpcAccrued_{self.name}_{wallet_address}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(self, wallet_address: str, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"pendingWpcAccrued_{self.name}_{wallet_address}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id) / 10 ** 18
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
                result[token]['borrow_amount_in_usd'] += borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] += deposit_amount_in_usd
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
                result[token]['borrow_amount_in_usd'] += borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] += deposit_amount_in_usd
        return result

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_distribution_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['distributionAddress'], self.distribution_abi, fn_name, fn_paras, block_number
        )

    def get_comptroller_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['comptrollerAddress'], self.comptroller_abi, fn_name, fn_paras, block_number
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
