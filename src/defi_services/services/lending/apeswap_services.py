import logging

from web3 import Web3

from defi_services.abis.lending.apeswape.apeswap_comptroller_abi import APESWAP_COMPTROLLER_ABI
from defi_services.abis.lending.apeswape.apeswap_lens_abi import APESWAP_LENS_ABI
from defi_services.abis.lending.apeswape.apswap_ctoken_abi import APESWAP_CTOKEN_ABI
from defi_services.constants.chain_constant import Chain, BlockTime
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.bsc.apeswap_bsc import APESWAP_BSC

logger = logging.getLogger("Compound Lending Pool State Service")


class ApeSwapInfo:
    mapping = {
        Chain.bsc: APESWAP_BSC
    }


class ApeSwapStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x38"):
        super().__init__(state_service, chain_id)
        self.comptroller_abi = APESWAP_COMPTROLLER_ABI
        self.lens_abi = APESWAP_LENS_ABI
        self.name = f"{self.chain_id}_{Lending.ape_swap}"
        self.pool_info = ApeSwapInfo.mapping.get(chain_id)

    def get_service_info(self):
        info = {
            Lending.ape_swap: {
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
        metadata = lens_contract.functions.cTokenMetadataAll(tokens).call(block_identifier=block_number)
        reserves_info = {}
        for data in metadata:
            underlying = data[13].lower()
            ctoken = data[0].lower()
            lt = data[10] / 10 ** 18
            ltv = data[10] / 10 ** 18

            underlying_decimal = int(data[15])
            exchange_rate = data[1] / 10 ** (18 - 8 + underlying_decimal)
            reserves_info[underlying] = {
                "cToken": ctoken,
                "exchangeRate": exchange_rate,
                "liquidationThreshold": lt,
                "loanToValue": ltv
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

        if self.chain_id == Chain.bsc:
            apx_block_speed_in_seconds = 1  # Change for ApeSwap Lending
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
        return {}

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        return {}

    def get_ctoken_function_info(self, ctoken: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            ctoken, APESWAP_CTOKEN_ABI, fn_name, fn_paras, block_number
        )
