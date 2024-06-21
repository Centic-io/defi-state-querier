import logging
from typing import List

from web3 import Web3

from defi_services.abis.lending.iron_bank.iron_comptroller_abi import IRON_COMPTROLLER_ABI
from defi_services.abis.lending.iron_bank.iron_lens_abi import IRON_LENS_ABI
from defi_services.abis.lending.iron_bank.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.blockchain.multicall_v2 import W3Multicall
from defi_services.services.lending.multicall_services.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.avalanche.iron_bank_avalanche import IRON_BANK_AVALANCHE
from defi_services.services.lending.lending_info.ethereum.iron_bank_eth import IRON_BANK_ETH
from defi_services.services.lending.lending_info.optimism.iron_bank_optimism import IRON_BANK_OPTIMISM

logger = logging.getLogger("Iron Bank Lending Pool State Service")


class IronBankInfo:
    mapping = {
        Chain.ethereum: IRON_BANK_ETH,
        Chain.optimism: IRON_BANK_OPTIMISM,
        Chain.avalanche: IRON_BANK_AVALANCHE
    }


class IronBankStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.iron_bank}"
        self.chain_id = chain_id
        self.pool_info = IronBankInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = IRON_LENS_ABI
        self.comptroller_abi = IRON_COMPTROLLER_ABI
        self.ctoken_abi = CTOKEN_ABI
        self._w3 = state_service.get_w3()

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.iron_bank: {
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
            # if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
            #              ContractAddresses.UST]:
            #     continue
            ctokens.append(token)

        lens_contract = _w3.eth.contract(
            address=Web3.to_checksum_address(self.pool_info.get("lensAddress")), abi=self.lens_abi
        )
        tokens = [Web3.to_checksum_address(i) for i in ctokens]
        reserves_info = {}
        queries = {}
        for token in tokens:
            key = f"underlying_{token}_latest".lower()
            queries[key] = {
                "address": token,
                "abi": self.ctoken_abi,
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
            underlying = decoded_data.get(key).lower()
            markets = f"markets_{token}_latest".lower()
            liquidation_threshold = decoded_data.get(markets)[1] / 10 ** 18

            if underlying != Token.native_token:
                underlying_contract = _w3.eth.contract(address=Web3.to_checksum_address(underlying), abi=ERC20_ABI)
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

    # PROTOCOL APY
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

        if self.chain_id == Chain.avalanche:
            apx_block_speed_in_seconds = 1  # Changed for Iron bank
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

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        if self.chain_id in [Chain.optimism, Chain.avalanche]:
            return {}
        multicall_call = self.get_comptroller_function_info("compAccrued", self._w3.to_checksum_address(wallet), block_number)
        return [multicall_call]

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        if self.chain_id in [Chain.optimism, Chain.avalanche]:
            return {}
        get_reward_id = f'compAccrued_{self.pool_info["comptrollerAddress"]}_{wallet}_{block_number}'.lower()
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
            health_factor: int = False
    ):
        multicall_calls: List['W3Multicall.Call'] = []
        wallet = self._w3.to_checksum_address(wallet)
        # Check asset is collateral
        multicall_calls.append(self.get_comptroller_function_info(
            fn_name='getAssetsIn', fn_paras=wallet, block_number=block_number))

        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get('cToken')
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            multicall_calls.append(self.get_ctoken_function_info(
                ctoken, "borrowBalanceCurrent", wallet, block_number))
            multicall_calls.append(self.get_ctoken_function_info(
                ctoken, "balanceOfUnderlying", wallet, block_number))
            multicall_calls.append(W3Multicall.Call(
                address=underlying, abi=ERC20_ABI, fn_name="decimals", block_number=block_number))

        return multicall_calls

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest",
            health_factor: int = False
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
        multicall_calls = self.get_wallet_deposit_borrow_balance_function_info(
            wallet,
            reserves_info,
            block_number,
            True
        )
        return multicall_calls

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
        multicall_calls: List['W3Multicall.Call'] = []
        for token, value in reserves_info.items():
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            ctoken = value.get('cToken')
            multicall_calls.append(self.get_ctoken_function_info(
                ctoken, "totalBorrows", block_number=block_number
            ))
            multicall_calls.append(self.get_ctoken_function_info(
                ctoken, "totalSupply", block_number=block_number
            ))
            multicall_calls.append(W3Multicall.Call(
                address=underlying, abi=ERC20_ABI, fn_name="decimals", block_number=block_number))
            multicall_calls.append(W3Multicall.Call(
                address=ctoken, abi=ERC20_ABI, fn_name="decimals", block_number=block_number))
            multicall_calls.append(self.get_ctoken_function_info(
                ctoken, "exchangeRateCurrent", block_number=block_number
            ))

        return multicall_calls

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
