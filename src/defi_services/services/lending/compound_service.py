import logging

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.constants.token_constant import ContractAddresses, Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.ethereum.compound_eth import COMPOUND_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Compound Lending Pool State Service")


class CompoundInfo:
    mapping = {
        Chain.ethereum: COMPOUND_ETH
    }


class CompoundStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__()
        self.name = f"{chain_id}_{Lending.compound}"
        self.chain_id = chain_id
        self.pool_info = CompoundInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = CREAM_LENS_ABI
        self.comptroller_abi = CREAM_COMPTROLLER_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.compound: {
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

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info_deprecated(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token, reserve_info in reserves_info.items():
            ctoken = reserve_info.get("ctoken")
            metadata_key = f"cTokenMetadata_{ctoken}_{block_number}".lower()
            rpc_calls[metadata_key] = self.get_lens_function_info('cTokenMetadata', [ctoken], block_number)

        return rpc_calls

    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, reserve_info in reserves_info.items():
            if token_address != Token.native_token:
                query_id = f"decimals_{token_address}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(token_address, ERC20_ABI, "decimals", [], block_number)

            ctoken = reserve_info.get("cToken")
            for fn_name in ['decimals', 'totalSupply', 'totalBorrows', 'supplyRatePerBlock', 'borrowRatePerBlock', 'exchangeRateStored']:
                query_id = f"{fn_name}_{ctoken}_{block_number}".lower()
                rpc_calls[query_id] = self.get_ctoken_function_info(
                    ctoken=ctoken,
                    fn_name=fn_name,
                    block_number=block_number
                )

        return rpc_calls

    @staticmethod
    def get_reserve_tokens_metadata_deprecated(
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token, reserve_info in reserves_info.items():
            ctoken = reserve_info.get('cToken')
            metadata_id = f"cTokenMetadata_{ctoken}_{block_number}".lower()
            info = decoded_data.get(metadata_id)

            reserve_tokens_info.append({
                "token": ctoken,
                "borrow_rate": info[3],
                "supply_rate": info[2],
                "supply": info[7],
                "borrow": info[5],
                "exchange_rate": info[1],
                "underlying": info[11].lower(),
                "underlying_decimals": info[13]
            })
        return reserve_tokens_info

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
                "supply_rate": decoded_data.get(supply_rate_query_id),
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

        data = {}
        for token_info in reserve_tokens_info:
            underlying_token = token_info['underlying']
            c_token = token_info['token']

            assets = {
                underlying_token: self._calculate_interest_rates(
                    token_info, pool_decimals=pool_decimals,
                    apx_block_speed_in_seconds=BlockTime.block_time_by_chains[self.chain_id]
                )
            }
            data[c_token] = assets

        return data

    @classmethod
    def _calculate_interest_rates(
            cls, token_info: dict, pool_decimals: int, apx_block_speed_in_seconds: float):
        block_per_day = int(TimeConstants.A_DAY / apx_block_speed_in_seconds)

        exchange_rate = float(token_info["exchange_rate"]) / 10 ** (18 - 8 + token_info["underlying_decimals"])

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

    @staticmethod
    def _calculate_interest_rates_deprecated(
            token_info: dict, pool_decimals: int, pool_price: float):
        apx_block_speed_in_seconds = 3
        exchange_rate = float(token_info["exchange_rate"]) / 10 ** (18 - 8 + token_info["underlying_decimals"])
        block_per_day = int(60 * 60 * 24 / apx_block_speed_in_seconds)
        venus_per_day = token_info["speed"] * block_per_day / 10 ** pool_decimals
        underlying_price = float(token_info["underlying_price"])
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
            'total_borrow': {
                DBConst.amount: total_borrow,
                DBConst.value_in_usd: total_borrow_usd
            },
            'total_deposit': {
                DBConst.amount: total_supply,
                DBConst.value_in_usd: total_supply_usd
            }
        }
        return {
            DBConst.reward_borrow_apy: borrow_apr,
            DBConst.reward_deposit_apy: supply_apr,
            'deposit_apy': supply_apy,
            'borrow_apy': borrow_apy,
            DBConst.liquidity_change_logs: liquidity_log,
            DBConst.mint_paused: token_info[DBConst.mint_paused],
            DBConst.borrow_paused: token_info[DBConst.borrow_paused]
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        reward_token = self.pool_info.get("rewardToken")
        comptroller = self.pool_info.get("comptrollerAddress")
        rpc_call = self.get_lens_function_info("getCompBalanceMetadataExt", [reward_token, comptroller, wallet], block_number)
        get_reward_id = f"getCompBalanceMetadataExt_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(self, decoded_data: dict, wallet: str, block_number: int = "latest"):
        get_reward_id = f"getCompBalanceMetadataExt_{self.name}_{wallet}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id)[-1] / 10 ** 18
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

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_comptroller_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        comptroller = self.pool_info['comptrollerAddress']
        return self.state_service.get_function_info(
            comptroller, self.comptroller_abi, fn_name, fn_paras, block_number
        )

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, CTOKEN_ABI, fn_name, fn_paras, block_number
        )
