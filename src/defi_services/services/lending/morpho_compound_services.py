import logging

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.lending.morpho.morpho_compound_comptroller_abi import MORPHO_COMPOUND_COMPTROLLER_ABI
from defi_services.abis.lending.morpho.morpho_compound_lens_abi import MORPHO_COMPOUND_LENS_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundInfo
from defi_services.services.lending.lending_info.ethereum.morpho_compound_eth import MORPHO_COMPOUND_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Compound Lending Pool State Service")


class MorphoCompoundInfo:
    mapping = {
        Chain.ethereum: MORPHO_COMPOUND_ETH
    }


class MorphoCompoundStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__()
        self.name = f"{chain_id}_{Lending.morpho_compound}"
        self.chain_id = chain_id
        self.compound_info = CompoundInfo.mapping.get(chain_id)
        self.pool_info = MorphoCompoundInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.compound_lens_abi = CREAM_LENS_ABI
        self.compound_comptroller_abi = CREAM_COMPTROLLER_ABI
        self.lens_abi = MORPHO_COMPOUND_LENS_ABI
        self.comptroller_abi = MORPHO_COMPOUND_COMPTROLLER_ABI
        self.market_key = 'cToken'

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.morpho_compound: {
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

        compound_lens_contract = _w3.eth.contract(
            address=Web3.toChecksumAddress(self.compound_info.get("lensAddress")), abi=self.compound_lens_abi
        )
        tokens = [Web3.toChecksumAddress(i) for i in ctokens]
        metadata = compound_lens_contract.functions.cTokenMetadataAll(tokens).call(block_identifier=block_number)
        reserves_info = {}
        for data in metadata:
            underlying = data[11].lower()
            ctoken = data[0].lower()
            lt = data[10] / 10 ** 18
            ltv = data[10] / 10 ** 18
            reserves_info[underlying] = {
                "cToken": ctoken,
                "liquidationThreshold": lt,
                "loanToValue": ltv
            }

        return reserves_info

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, value in reserves_info.items():
            if token_address != Token.native_token:
                decimals_key = f"decimals_{token_address}_{block_number}".lower()
                rpc_calls[decimals_key] = self.state_service.get_function_info(
                    token_address, ERC20_ABI, "decimals", block_number=block_number)

            c_token = value['cToken']
            market_data_query_id = f"getMainMarketData_{self.name}_{c_token}_{block_number}".lower()
            rpc_calls[market_data_query_id] = self.get_lens_function_info(
                'getMainMarketData', [c_token], block_number=block_number)

            ctoken = value.get("cToken")
            for fn_name in ['supplyRatePerBlock', 'borrowRatePerBlock']:
                query_id = f"{fn_name}_{ctoken}_{block_number}".lower()
                rpc_calls[query_id] = self.get_ctoken_function_info(
                    ctoken=ctoken,
                    fn_name=fn_name,
                    block_number=block_number
                )

        return rpc_calls

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

            supply_rate_query_id = f"supplyRatePerBlock_{ctoken}_{block_number}".lower()
            borrow_rate_query_id = f"borrowRatePerBlock_{ctoken}_{block_number}".lower()

            market_data_query_id = f"getMainMarketData_{self.name}_{ctoken}_{block_number}".lower()
            market_data = decoded_data.get(market_data_query_id)

            reserve_tokens_info.append({
                'underlying': token_address,
                'underlying_decimals': underlying_decimals,
                "borrow_rate": decoded_data.get(borrow_rate_query_id),
                "supply_rate": decoded_data.get(supply_rate_query_id),
                'p2p_supply': market_data[2],
                'p2p_borrow': market_data[3],
                'pool_supply': market_data[4],
                'pool_borrow': market_data[5]
            })

        return reserve_tokens_info

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ):
        reserve_tokens_info = self.get_reserve_tokens_metadata(decoded_data, reserves_info, block_number)

        data = {}
        for token_info in reserve_tokens_info:
            underlying_token = token_info['underlying']
            data[underlying_token] = self._calculate_interest_rates(
                token_info, pool_decimals=pool_decimals,
                apx_block_speed_in_seconds=BlockTime.block_time_by_chains[self.chain_id]
            )

        return {self.pool_info.get("comptrollerAddress"): data}

    @classmethod
    def _calculate_interest_rates(cls, token_info: dict, pool_decimals: int, apx_block_speed_in_seconds: int):
        block_per_day = int(TimeConstants.A_DAY / apx_block_speed_in_seconds)

        decimals = token_info['underlying_decimals']
        total_supply = float(token_info["p2p_supply"]) / 10 ** decimals + float(token_info["pool_supply"]) / 10 ** decimals
        total_borrow = float(token_info["p2p_borrow"]) / 10 ** decimals + float(token_info["pool_borrow"]) / 10 ** decimals

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
            block_number: int = "latest"
    ):
        if not reserves_info:
            reserves_info = self.pool_info.get("reservesList")
        params = [
            [Web3.toChecksumAddress(value.get(self.market_key)) for key, value in reserves_info.items()],
            Web3.toChecksumAddress(wallet)
        ]
        rpc_call = self.get_lens_function_info("getUserUnclaimedRewards", params, block_number)
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet}_{block_number}".lower()
        return {get_reward_id: rpc_call}

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet}_{block_number}".lower()
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
            ctoken = value.get(self.market_key)
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            underlying_borrow_key = f"getCurrentBorrowBalanceInOf_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            underlying_balance_key = f"getCurrentSupplyBalanceInOf_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_borrow_key] = self.get_lens_function_info(
                "getCurrentBorrowBalanceInOf", [ctoken, wallet], block_number)
            rpc_calls[underlying_balance_key] = self.get_lens_function_info(
                "getCurrentSupplyBalanceInOf", [ctoken, wallet], block_number)
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
        total_borrow, total_collateral = 0, 0
        pool_address = self.pool_info.get("comptrollerAddress")
        for token, value in reserves_info.items():
            data = {}
            underlying = token
            ctoken = value.get(self.market_key)
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            get_total_deposit_id = f"getCurrentSupplyBalanceInOf_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            get_total_borrow_id = f"getCurrentBorrowBalanceInOf_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            deposit_amount = decoded_data[get_total_deposit_id][-1] / 10 ** decimals
            borrow_amount = decoded_data[get_total_borrow_id][-1] / 10 ** decimals
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
                total_collateral += deposit_amount_in_usd * value.get("liquidationThreshold")
            result.update(data)
        result = {pool_address.lower(): result}
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

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_comptroller_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['comptrollerAddress'], self.comptroller_abi, fn_name, fn_paras, block_number
        )

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, CTOKEN_ABI, fn_name, fn_paras, block_number
        )
