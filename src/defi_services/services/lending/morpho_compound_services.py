import logging
import time

from web3 import Web3

from defi_services.abis.lending.cream.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.lending.morpho.morpho_compound_comptroller_abi import MORPHO_COMPOUND_COMPTROLLER_ABI
from defi_services.abis.lending.morpho.morpho_compound_lens_abi import MORPHO_COMPOUND_LENS_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import ContractAddresses, Token
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
            if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
                         ContractAddresses.UST]:
                continue
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
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"
    ):
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
