import logging
import time

from web3 import Web3

from defi_services.abis.lending.liqee.liqee_comptroller_abi import LIQEE_CONTROLLER_ABI
from defi_services.abis.lending.liqee.liqee_lending_data_abi import LIQEE_LENDING_DATA_ABI
from defi_services.abis.lending.liqee.liqee_token_abi import LIQEE_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.bsc.liqee_bsc import LIQEE_BSC
from defi_services.services.lending.lending_info.ethereum.liqee_eth import LIQEE_ETH

logger = logging.getLogger("Liqee Lending Pool State Service")


class LiqeeInfo:
    mapping = {
        Chain.ethereum: LIQEE_ETH,
        Chain.bsc: LIQEE_BSC
    }


class LiqeeStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.liqee}"
        self.chain_id = chain_id
        self.pool_info = LiqeeInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lending_data_abi = LIQEE_LENDING_DATA_ABI
        self.controller_abi = LIQEE_CONTROLLER_ABI
        self.lquee_token_abi = LIQEE_TOKEN_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.liqee: {
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
            address=_w3.toChecksumAddress(self.pool_info.get("controllerAddress")), abi=self.controller_abi)
        ctokens = []
        for token in comptroller_contract.functions.getAlliTokens().call(block_identifier=block_number):
            ctokens.append(token)
        reserves_info = {}
        for token in ctokens:
            address = _w3.toChecksumAddress(token)
            contract = _w3.eth.contract(address=address, abi=self.lquee_token_abi)
            underlying = contract.functions.underlying().call(block_identifier=block_number)
            liquidation_threshold = comptroller_contract.functions.markets(address).call(block_identifier=block_number)
            liquidation_threshold = liquidation_threshold[0] / 10 ** 18

            exchange_rate = contract.functions.exchangeRateStored().call(block_identifier=block_number)
            exchange_rate = exchange_rate / 10 ** 18

            reserves_info[underlying.lower()] = {
                "cToken": token.lower(),
                "exchangeRate": exchange_rate,
                "liquidationThreshold": liquidation_threshold,
                "loanToValue": liquidation_threshold
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

    # CALCULATE APY LENDING POOL
    def get_reserve_tokens_metadata(
            self,
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token_address, reserve_info in reserves_info.items():
            if token_address != Token.native_token:
                underlying_decimals_query_id = f"decimals_{token_address}_{block_number}".lower()
                underlying_decimals = decoded_data.get(underlying_decimals_query_id)
            else:
                underlying_decimals = Chain.native_decimals.get(self.chain_id, 18)

            ctoken = reserve_info.get("cToken")
            ctoken_decimals_query_id = f"decimals_{ctoken}_{block_number}".lower()
            total_supply_query_id = f"totalSupply_{ctoken}_{block_number}".lower()
            total_borrow_query_id = f"totalBorrows_{ctoken}_{block_number}".lower()
            supply_rate_query_id = f"supplyRatePerBlock_{ctoken}_{block_number}".lower()
            borrow_rate_query_id = f"borrowRatePerBlock_{ctoken}_{block_number}".lower()
            exchange_rate_query_id = f"exchangeRateStored_{ctoken}_{block_number}".lower()

            reserve_tokens_info.append({
                "token": ctoken,
                "token_decimals": decoded_data.get(ctoken_decimals_query_id),
                "borrow_rate": decoded_data.get(borrow_rate_query_id),
                "supply_rate": decoded_data.get(supply_rate_query_id) or 0,  # dForce iMUSX 0x36f4c36d1f6e8418ecb2402f896b2a8fedde0991 does not support function supplyRatePerBlock
                "supply": decoded_data.get(total_supply_query_id),
                "borrow": decoded_data.get(total_borrow_query_id),
                "exchange_rate": decoded_data.get(exchange_rate_query_id),
                "underlying_decimals": underlying_decimals,
                "underlying": token_address
            })
        return reserve_tokens_info

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = "latest",
    ):
        reserve_tokens_info = self.get_reserve_tokens_metadata(decoded_data, reserves_info, block_number)

        if self.chain_id == Chain.ethereum:
            apx_block_speed_in_seconds = 13  # Follow document of dForce
        else:
            apx_block_speed_in_seconds = BlockTime.block_time_by_chains[self.chain_id]

        data = {}
        for token_info in reserve_tokens_info:
            underlying_token = token_info['underlying']
            c_token = token_info['token']

            assets = {
                underlying_token: self._calculate_interest_rates(
                    token_info, pool_decimals=pool_decimals,
                    apx_block_speed_in_seconds=apx_block_speed_in_seconds
                )
            }
            data[c_token] = assets

        return data

    @classmethod
    def _calculate_interest_rates(
            cls, token_info: dict, pool_decimals: int, apx_block_speed_in_seconds: float):
        block_per_day = int(TimeConstants.A_DAY / apx_block_speed_in_seconds)

        exchange_rate = float(token_info["exchange_rate"]) / 10 ** 18  # changed for dForce

        total_borrow = float(token_info["borrow"]) / 10 ** int(token_info["underlying_decimals"])
        total_supply = float(token_info["supply"]) * exchange_rate / 10 ** int(token_info["token_decimals"])

        supply_apy = ((token_info["supply_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1
        borrow_apy = ((token_info["borrow_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1

        return {
            'deposit_apy': supply_apy,
            'borrow_apy': borrow_apy,
            'total_deposit': total_supply,
            'total_borrow': total_borrow
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        fn_paras = [Web3.toChecksumAddress(wallet)]
        rpc_call = self.get_lending_function_info("getAccountRewardAmount", fn_paras, block_number)
        get_reward_id = f"getAccountRewardAmount_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"getAccountRewardAmount_{self.name}_{wallet}_{block_number}".lower()
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
            health_factor: bool = False):
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
                "is_collateral": True if value.get('liquidationThreshold') > 0 else False
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
                result['health_factor'] = total_collateral / total_borrow
            elif total_collateral:
                result['health_factor'] = 100
            else:
                result['health_factor'] = 0
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
                result[token]['borrow_amount_in_usd'] = borrow_amount_in_usd
                result[token]['deposit_amount_in_usd'] = deposit_amount_in_usd
        return result

    def get_lending_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lendingDataAddress'], self.lending_data_abi, fn_name, fn_paras, block_number
        )
