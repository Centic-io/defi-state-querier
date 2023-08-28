from web3 import Web3

from defi_services.abis.lending.venus.venus_comptroller_abi import VENUS_COMPTROLLER_ABI
from defi_services.abis.lending.venus.venus_lens_abi import VENUS_LENS_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.bsc.venus_bsc import VENUS_BSC


class VenusInfo:
    mapping = {
        Chain.bsc: VENUS_BSC
    }


class VenusStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x38"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_venus"
        self.chain_id = chain_id
        self.pool_info = VenusInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = VENUS_LENS_ABI
        self.comptroller_abi = VENUS_COMPTROLLER_ABI

        # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            "venus": {
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
        metadata = lens_contract.functions.vTokenMetadataAll(tokens).call(block_identifier=block_number)
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

    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
            is_price_oracle: bool = False
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            ctoken = value.get("ctoken")
            speed_key = f"venusSpeeds_{ctoken}_{block_number}".lower()
            mint_key = f"mintGuardianPaused_{ctoken}_{block_number}".lower()
            borrow_key = f"borrowGuardianPaused_{token}_{block_number}".lower()
            metadata_key = f"vTokenMetadata_{token}_{block_number}".lower()
            if is_price_oracle:
                price_key = f"vTokenUnderlyingPrice_{token}_{block_number}".lower()
                rpc_calls[price_key] = self.get_comptroller_function_info(
                    'vTokenUnderlyingPrice', [ctoken], block_number)
            rpc_calls[speed_key] = self.get_comptroller_function_info('venusSpeeds', [ctoken], block_number)
            rpc_calls[mint_key] = self.get_comptroller_function_info('mintGuardianPaused', [ctoken], block_number)
            rpc_calls[borrow_key] = self.get_comptroller_function_info('borrowGuardianPaused', [ctoken], block_number)
            rpc_calls[metadata_key] = self.get_comptroller_function_info('vTokenMetadata', [ctoken], block_number)

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
            speeds_call_id = f'venusSpeeds_{ctoken}_{block_number}'.lower()
            borrow_guardian_paused_call_id = f'borrowGuardianPaused_{ctoken}_{block_number}'.lower()
            mint_guardian_paused_call_id = f'mintGuardianPaused_{ctoken}_{block_number}'.lower()
            ctoken_speeds[ctoken] = decoded_data.get(speeds_call_id)
            borrow_paused_tokens[ctoken] = decoded_data.get(borrow_guardian_paused_call_id)
            mint_paused_tokens[ctoken] = decoded_data.get(mint_guardian_paused_call_id)
            metadata_id = f"vTokenMetadata_{ctoken}_{block_number}".lower()
            reserve_tokens_info.append(decoded_data.get(metadata_id))
            if is_oracle_price:
                underlying_id = f"vTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
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

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        fn_paras = [
            Web3.toChecksumAddress(wallet_address),
            Web3.toChecksumAddress(self.pool_info.get("comptrollerAddress"))
        ]
        rpc_call = self.get_lens_function_info("pendingVenus", fn_paras, block_number)
        get_reward_id = f"pendingVenus_{wallet_address}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(self, wallet_address: str, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"pendingVenus_{wallet_address}_{block_number}".lower()
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
            underlying_price_key = f"vTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
            underlying_borrow_key = f"borrowBalanceCurrent_{ctoken}_{wallet_address}_{block_number}".lower()
            underlying_balance_key = f"balanceOfUnderlying_{ctoken}_{wallet_address}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            if is_oracle_price:
                rpc_calls[underlying_price_key] = self.get_lens_function_info(
                    "vTokenUnderlyingPrice", [ctoken], block_number)
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
                get_underlying_token_price = f"vTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
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

    #TOKEN DEPOSIT BORROW BALANCE
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
            underlying_price_key = f"vTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
            underlying_borrow_key = f"totalBorrows_{ctoken}_{block_number}".lower()
            underlying_balance_key = f"totalSupply_{ctoken}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            ctoken_decimals_key = f"decimals_{ctoken}_{block_number}".lower()
            exchange_rate_key = f"exchangeRateCurrent_{ctoken}_{block_number}".lower()
            if is_oracle_price:
                rpc_calls[underlying_price_key] = self.get_lens_function_info(
                    "vTokenUnderlyingPrice", [ctoken], block_number)
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
                get_underlying_token_price = f"vTokenUnderlyingPrice_{ctoken}_{block_number}".lower()
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

    def get_ctoken_metadata_all(
            self,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"vTokenMetadataAll_{self.pool_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("vTokenMetadataAll", tokens, block_number)
        }

    def ctoken_underlying_price_all(
            self, reserves_info, block_number: int = 'latest'):
        tokens = [Web3.toChecksumAddress(value['cToken']) for key, value in reserves_info.items()]
        key = f"vTokenUnderlyingPriceAll_{self.pool_info.get('lensAddress')}_{block_number}".lower()
        return {
            key: self.get_lens_function_info("cTokenUnderlyingPriceAll", tokens, block_number)
        }