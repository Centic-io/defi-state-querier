import logging
import time

from web3 import Web3

from defi_services.abis.lending.aave_v2_and_forlks.aave_v2_incentives_abi import AAVE_V2_INCENTIVES_ABI
from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.morpho.morpho_aave_v2_comptroller_abi import MORPHO_AAVE_V2_COMPTROLLER
from defi_services.abis.lending.morpho.morpho_aave_v2_lens_abi import MORPHO_AAVE_V2_LENS_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.aave_v2_services import AaveInfo
from defi_services.services.lending.lending_info.ethereum.morpho_aave_v2_eth import MORPHO_AAVE_V2_ETH
from defi_services.services.lending.morpho_compound_services import MorphoCompoundStateService

logger = logging.getLogger("Compound Lending Pool State Service")


class MorphoAaveV2Info:
    mapping = {
        Chain.ethereum: MORPHO_AAVE_V2_ETH
    }


class MorphoAaveV2StateService(MorphoCompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.morpho_aave_v2}"
        self.chain_id = chain_id
        self.compound_info = AaveInfo.mapping.get(chain_id)
        self.pool_info = MorphoAaveV2Info.mapping.get(chain_id)
        self.state_service = state_service
        self.lending_abi = LENDING_POOL_ABI
        self.incentive_abi = AAVE_V2_INCENTIVES_ABI
        self.oracle_abi = ORACLE_ABI
        self.lens_abi = MORPHO_AAVE_V2_LENS_ABI
        self.comptroller_abi = MORPHO_AAVE_V2_COMPTROLLER
        self.market_key = 'tToken'

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.morpho_aave_v2: {
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
        pool_address = Web3.toChecksumAddress(self.pool_info['address'])
        contract = _w3.eth.contract(address=pool_address, abi=self.lending_abi)
        comptroller_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.pool_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        markets = comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number)
        reserves_list = contract.functions.getReservesList().call(block_identifier=block_number)
        reserves_info = {}
        for token in reserves_list:
            value = contract.functions.getReserveData(token).call(block_identifier=block_number)
            key = token.lower()
            ttoken = value[7]
            if ttoken in markets:
                reserves_info[key] = {}
                reserves_info[key]["tToken"] = ttoken.lower()
                reserves_info[key]["dToken"] = value[9].lower()
                reserves_info[key]["sdToken"] = value[8].lower()
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

    def calculate_rewards_balance(self, decoded_data: dict, wallet: str, block_number: int = "latest"):
        return {}
