import logging

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.ethereum.flux_eth import FLUX_ETH

logger = logging.getLogger("Flux finance Lending Pool State Service")


class FluxInfo:
    mapping = {
        Chain.ethereum: FLUX_ETH
    }


class FluxStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.flux}"
        self.chain_id = chain_id
        self.pool_info = FluxInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = CREAM_LENS_ABI
        self.comptroller_abi = CREAM_COMPTROLLER_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.flux: {
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

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        rpc_call = self.get_comptroller_function_info("compAccrued", [wallet], block_number)
        get_reward_id = f"compAccrued_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        get_reward_id = f"compAccrued_{self.name}_{wallet}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id) / 10 ** 18
        reward_token = self.pool_info.get("rewardToken")
        result = {
            reward_token: {"amount": rewards}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            health_factor: bool = False
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get('cToken')
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            underlying_borrow_key = f"borrowBalanceCurrent_{ctoken}_{wallet}_{block_number}".lower()
            underlying_balance_key = f"balanceOfUnderlying_{ctoken}_{wallet}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_borrow_key] = self.get_ctoken_function_info(
                ctoken, "borrowBalanceCurrent", [wallet], block_number)
            rpc_calls[underlying_balance_key] = self.get_ctoken_function_info(
                ctoken, "balanceOfUnderlying", [wallet], block_number)
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, ERC20_ABI, "decimals", [], block_number
            )

        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest",
            health_factor: bool = False
    ):
        if token_prices is None:
            token_prices = {}
        result = {}
        total_borrow = 0
        total_collateral = 0
        for token, value in reserves_info.items():
            data = {}
            underlying = token
            ctoken = value.get("cToken")
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            get_total_deposit_id = f"balanceOfUnderlying_{ctoken}_{wallet}_{block_number}".lower()
            get_total_borrow_id = f"borrowBalanceCurrent_{ctoken}_{wallet}_{block_number}".lower()
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            deposit_amount = decoded_data[get_total_deposit_id] / 10 ** decimals
            borrow_amount = decoded_data[get_total_borrow_id] / 10 ** decimals
            data[token] = {
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
                data[token]['borrow_amount_in_usd'] = borrow_amount_in_usd
                data[token]['deposit_amount_in_usd'] = deposit_amount_in_usd
                total_borrow += borrow_amount_in_usd
                total_collateral += deposit_amount_in_usd * value.get("liquidationThreshold")
            result[ctoken] = data
        if health_factor:
            if total_collateral and total_borrow:
                result['health_factor'] = total_collateral/total_borrow
            elif total_collateral:
                result['health_factor'] = 100
            else:
                result['health_factor'] = 0

        return result

    # TOKEN DEPOSIT BORROW BALANCE
    def get_token_deposit_borrow_balance_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
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
                result[token]['borrow_amount_in_usd'] = borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] = deposit_amount_in_usd
        return result

    # HEALTH FACTOR
    def get_health_factor_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = self.get_wallet_deposit_borrow_balance_function_info(
            wallet,
            reserves_info,
            block_number,
            True
        )
        return rpc_calls

    def calculate_health_factor(
            self,
            wallet: str,
            reserves_info,
            decoded_data: dict = None,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest"
    ):
        data = self.calculate_wallet_deposit_borrow_balance(
            wallet,
            reserves_info,
            decoded_data,
            token_prices,
            pool_decimals,
            block_number,
            True
        )

        return {"health_factor": data["health_factor"]}
