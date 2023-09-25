import logging
import time

from web3 import Web3

from defi_services.abis.lending.aave_v2_and_forlks.aave_v2_incentives_abi import AAVE_V2_INCENTIVES_ABI
from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.morpho.morpho_aave_v3_comptroller_abi import MORPHO_AAVE_V3_COMPTROLLER_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v3_services import AaveV3Info
from defi_services.services.lending.lending_info.ethereum.morpho_aave_v3_eth import MORPHO_AAVE_V3_ETH
from defi_services.services.lending.morpho_compound_services import MorphoCompoundStateService

logger = logging.getLogger("Compound Lending Pool State Service")


class MorphoAaveV3Info:
    mapping = {
        Chain.ethereum: MORPHO_AAVE_V3_ETH
    }


class MorphoAaveV3StateService(MorphoCompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.morpho_aave_v3}"
        self.chain_id = chain_id
        self.aave_info = AaveV3Info.mapping.get(chain_id)
        self.pool_info = MorphoAaveV3Info.mapping.get(chain_id)
        self.state_service = state_service
        self.lending_abi = LENDING_POOL_ABI
        self.incentive_abi = AAVE_V2_INCENTIVES_ABI
        self.oracle_abi = ORACLE_ABI
        self.comptroller_abi = MORPHO_AAVE_V3_COMPTROLLER_ABI
        self.market_key = 'tToken'

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.morpho_aave_v3: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(
            self,
            block_number: int = "latest"):
        begin = time.time()
        _w3 = self.state_service.get_w3()
        pool_address = Web3.toChecksumAddress(self.aave_info['address'])
        contract = _w3.eth.contract(address=pool_address, abi=self.lending_abi)
        comptroller_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.pool_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        markets = comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number)
        markets = [i.lower() for i in markets]
        reserves_list = contract.functions.getReservesList().call(block_identifier=block_number)
        reserves_info = {}
        for token in reserves_list:
            value = contract.functions.getReserveData(token).call(block_identifier=block_number)
            key = token.lower()
            if token in markets:
                reserves_info[key] = {}
                reserves_info[key]["tToken"] = value[8].lower()
                reserves_info[key]["dToken"] = value[9].lower()
                reserves_info[key]["sdToken"] = value[10].lower()
                risk_param = bin(value[0][0])[2:]
                reserves_info[key]["liquidationThreshold"] = int(risk_param[-31:-16], 2) / 10 ** 4
        logger.info(f"Get reserves information in {time.time() - begin}s")
        return reserves_info

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        return {}

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        return {}

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest"
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            ctoken = value.get(self.market_key)
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            underlying_borrow_key = f"borrowBalance_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            underlying_balance_key = f"collateralBalance_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            underlying_decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[underlying_borrow_key] = self.get_comptroller_function_info(
                "borrowBalance", [token, wallet], block_number)
            rpc_calls[underlying_balance_key] = self.get_comptroller_function_info(
                "collateralBalance", [token, wallet], block_number)
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
            block_number: int = "latest"
    ):
        if token_prices is None:
            token_prices = {}
        result = {}
        pool_address = self.pool_info.get("comptrollerAddress")
        for token, value in reserves_info.items():
            data = {}
            underlying = token
            ctoken = value.get(self.market_key)
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            get_total_deposit_id = f"collateralBalance_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
            get_total_borrow_id = f"borrowBalance_{self.name}_{ctoken}_{wallet}_{block_number}".lower()
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
                data[token]['borrow_amount_in_usd'] += borrow_amount_in_usd
                data[token]['deposit_amount_in_usd'] += deposit_amount_in_usd
            result.update(data)
        return {pool_address.lower(): result}
