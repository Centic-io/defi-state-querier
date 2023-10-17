import logging
import time

from web3 import Web3

from defi_services.abis.lending.aave_v2_and_forlks.aave_v2_incentives_abi import AAVE_V2_INCENTIVES_ABI
from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.morpho.morpho_aave_v2_comptroller_abi import MORPHO_AAVE_V2_COMPTROLLER
from defi_services.abis.lending.morpho.morpho_aave_v2_lens_abi import MORPHO_AAVE_V2_LENS_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v2_services import AaveInfo
from defi_services.services.lending.lending_info.ethereum.morpho_aave_v2_eth import MORPHO_AAVE_V2_ETH
from defi_services.services.lending.morpho_compound_services import MorphoCompoundStateService
from defi_services.utils.apy import apr_to_apy

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
        self.aave_info = AaveInfo.mapping.get(chain_id)
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
        pool_address = Web3.toChecksumAddress(self.aave_info['address'])
        contract = _w3.eth.contract(address=pool_address, abi=self.lending_abi)
        comptroller_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.pool_info.get("comptrollerAddress")), abi=self.comptroller_abi)
        markets = comptroller_contract.functions.getMarketsCreated().call(block_identifier=block_number)
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

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, value in reserves_info.items():
            decimals_key = f"decimals_{token_address}_{block_number}".lower()
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token_address, ERC20_ABI, "decimals", block_number=block_number)

            a_token = value['tToken']
            market_data_query_id = f"getMainMarketData_{self.name}_{a_token}_{block_number}".lower()
            rpc_calls[market_data_query_id] = self.get_lens_function_info(
                'getMainMarketData', [a_token], block_number=block_number)

            reserve_key = f"getReserveData_{self.name}_{token_address}_{block_number}".lower()
            rpc_calls[reserve_key] = self.get_function_lending_pool_info("getReserveData", [token_address])

        return rpc_calls

    def get_reserve_tokens_metadata(
            self,
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token_address, reserve_info in reserves_info.items():
            get_reserve_data_call_id = f'getReserveData_{self.name}_{token_address}_{block_number}'.lower()
            reserve_data = decoded_data.get(get_reserve_data_call_id)

            a_token = reserve_data[7].lower()
            market_data_query_id = f"getMainMarketData_{self.name}_{a_token}_{block_number}".lower()
            market_data = decoded_data.get(market_data_query_id)

            decimals_call_id = f"decimals_{token_address}_{block_number}".lower()

            reserve_tokens_info.append({
                'underlying': token_address,
                'underlying_decimals': decoded_data.get(decimals_call_id),
                'supply_apy': reserve_data[3],
                'borrow_apy': reserve_data[4],
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
            data[underlying_token] = self._calculate_interest_rates(token_info)

        return data

    @classmethod
    def _calculate_interest_rates(cls, token_info: dict):
        decimals = token_info['underlying_decimals']
        total_supply = float(token_info["p2p_supply"]) / 10 ** decimals + float(token_info["pool_supply"]) / 10 ** decimals
        total_borrow = float(token_info["p2p_borrow"]) / 10 ** decimals + float(token_info["pool_borrow"]) / 10 ** decimals

        supply_apr = float(token_info['supply_apy']) / 10 ** 27
        supply_apy = apr_to_apy(supply_apr)
        borrow_apr = float(token_info['borrow_apy']) / 10 ** 27
        borrow_apy = apr_to_apy(borrow_apr)

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
        return {}

    def calculate_rewards_balance(self, decoded_data: dict, wallet: str, block_number: int = "latest"):
        return {}

    def get_function_lending_pool_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.aave_info['address'], self.lending_abi, fn_name, fn_paras, block_number
        )

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )
