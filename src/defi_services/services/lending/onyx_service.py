import logging

from web3 import Web3

from defi_services.abis.lending.onyx.onyx_comptroller_abi import ONYX_COMPTROLLER_ABI
from defi_services.abis.lending.onyx.onyx_lens_abi import ONYX_LENS_ABI
from defi_services.abis.lending.onyx.onyx_token_abi import ONYX_TOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.ethereum.onyx_eth import ONYX_ETH

logger = logging.getLogger("Onyx Lending Pool State Service")


class OnyxInfo:
    mapping = {
        Chain.ethereum: ONYX_ETH
    }


class OnyxStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.onyx}"
        self.chain_id = chain_id
        self.pool_info = OnyxInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = ONYX_LENS_ABI
        self.comptroller_abi = ONYX_COMPTROLLER_ABI
        self.token_abi = ONYX_TOKEN_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.onyx: {
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
            # if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
            #              ContractAddresses.UST]:
            #     continue
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
            ltv = data[10] / 10 ** 18

            underlying_decimal = int(data[13])
            exchange_rate = data[1] / 10 ** (18 - 8 + underlying_decimal)

            reserves_info[underlying] = {
                "cToken": ctoken,
                "exchangeRate": exchange_rate,
                "liquidationThreshold": lt,
                "loanToValue": ltv
            }

        return reserves_info

    # PROTOCOL APY
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

            ctoken_decimals = decoded_data.get(ctoken_decimals_query_id)
            reserve_tokens_info.append({
                "token": ctoken,
                "token_decimals": ctoken_decimals,
                "borrow_rate": decoded_data.get(borrow_rate_query_id),
                "supply_rate": decoded_data.get(supply_rate_query_id),
                "supply": decoded_data.get(total_supply_query_id),
                "borrow": decoded_data.get(total_borrow_query_id),
                "exchange_rate": decoded_data.get(exchange_rate_query_id),
                "underlying_decimals": underlying_decimals or 8,  # Onyx protocol support NFT as reserves
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
            apx_block_speed_in_seconds = 15  # Changed for onyx protocol
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
        rpc_call = self.get_comptroller_function_info("xcnAccrued", [wallet], block_number)
        get_reward_id = f"xcnAccrued_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"xcnAccrued_{self.name}_{wallet}_{block_number}".lower()
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

            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            if value.get("decimals"):
                continue
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_decimals_key] = self.state_service.get_function_info(
                underlying, ERC20_ABI, "decimals", [], block_number
            )
            key = f"oTokenBalances_{self.name}_{wallet}_{token}_{block_number}".lower()
            rpc_calls[key] = self.get_lens_function_info(
                "oTokenBalances", [value.get("cToken"), Web3.toChecksumAddress(wallet)])
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
        total_borrow, total_collateral = 0, 0
        for token, value in reserves_info.items():
            key = f"oTokenBalances_{self.name}_{wallet}_{token}_{block_number}".lower()
            ctoken_balance = decoded_data.get(key)
            data = {}
            underlying = token
            ctoken = value.get("cToken")
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)

            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data.get(get_decimals_id, 0)
            deposit_amount = ctoken_balance[3] / 10 ** decimals
            borrow_amount = ctoken_balance[2] / 10 ** decimals
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
                hf = total_collateral / total_borrow
            elif total_collateral:
                hf = 100
            else:
                hf = 0
            result["health_factor"] = hf
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
