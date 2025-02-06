from web3 import Web3

from defi_services.abis.lending.justlend.just_token_abi import JUST_TOKEN_ABI
from defi_services.abis.lending.justlend.justlend_comptroller_abi import JUSTLEND_COMPTROLLER_ABI
from defi_services.abis.token.trc20_abi import TRC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.tron.justlend_tron import JUSTLEND_TRON


class JustLendInfo:
    mapping = {
        Chain.tron: JUSTLEND_TRON
    }


class JustLendStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x2b6653dc"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.justlend}"
        self.chain_id = chain_id
        self.pool_info = JustLendInfo.mapping.get(chain_id)
        self.comptroller_abi = JUSTLEND_COMPTROLLER_ABI

        # BASIC FUNCTIONS

    def get_service_info(self):
        info = {
            Lending.justlend: {
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
            address=_w3.to_checksum_address(self.pool_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        ctokens = []
        for token in comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number):
            ctokens.append(token)

        tokens = [Web3.to_checksum_address(i) for i in ctokens]
        reserves_info = {}
        queries = {}
        for token in tokens:
            key = f"underlying_{token}_latest".lower()
            queries[key] = {
                "address": token,
                "abi": JUST_TOKEN_ABI,
                "params": [],
                "function": "underlying",
                "block_number": "latest"
            }

            exchange_rate_query_id = f'exchangeRateStored_{token}_{block_number}'
            queries[exchange_rate_query_id] = self.get_ctoken_function_info(
                ctoken=token, fn_name='exchangeRateStored', block_number=block_number)

            markets = f"markets_{token}_latest".lower()
            queries[markets] = self.get_comptroller_function_info("markets", [token])
        decoded_data = self.state_service.query_state_data(queries)
        for token in tokens:
            key = f"underlying_{token}_latest".lower()
            markets = f"markets_{token}_latest".lower()
            underlying = decoded_data.get(key).lower()
            liquidation_threshold = decoded_data.get(markets)[1] / 10 ** 18

            if underlying != Token.native_token:
                underlying_contract = _w3.eth.contract(address=Web3.to_checksum_address(underlying), abi=TRC20_ABI)
                underlying_decimal = underlying_contract.functions.decimals().call()

            else:
                underlying_decimal = Chain.native_decimals.get(self.chain_id, 18)
            exchange_rate_query_id = f'exchangeRateStored_{token}_{block_number}'
            exchange_rate = decoded_data.get(exchange_rate_query_id) / 10 ** (18 - 8 + underlying_decimal)

            reserves_info[underlying] = {
                'cToken': token.lower(),
                "exchangeRate": exchange_rate,
                "liquidationThreshold": liquidation_threshold,
                "loanToValue": liquidation_threshold
            }
        return reserves_info

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        rpc_call = self.get_comptroller_function_info("compAccrued", [wallet])
        get_reward_id = f"compAccrued_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
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

        # Check asset is collateral
        assets_in_query_id = f"getAssetsIn_{self.pool_info['comptrollerAddress']}_{wallet}_{block_number}".lower()
        rpc_calls[assets_in_query_id] = self.get_comptroller_function_info(
            fn_name='getAssetsIn', fn_paras=[wallet], block_number=block_number)

        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get('cToken')
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            underlying_borrow_key = f"borrowBalanceCurrent_{ctoken}_{wallet}_{block_number}".lower()
            underlying_balance_key = f"balanceOfUnderlying_{ctoken}_{wallet}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_borrow_key] = self.get_ctoken_function_info(
                ctoken, "borrowBalanceCurrent", [wallet])
            rpc_calls[underlying_balance_key] = self.get_ctoken_function_info(
                ctoken, "balanceOfUnderlying", [wallet])
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, TRC20_ABI, "decimals", []
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
        assets_in_query_id = f"getAssetsIn_{self.pool_info['comptrollerAddress']}_{wallet}_{block_number}".lower()
        assets_in = [t.lower() for t in decoded_data[assets_in_query_id]]

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
                "is_collateral": ctoken in assets_in
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
                if data[token]['isCollateral']:
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
