from web3 import Web3

from defi_services.abis.lending.justlend.just_token_abi import JUST_TOKEN_ABI
from defi_services.abis.token.ctoken_abi import CTOKEN_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.tron.justlend_tron import JUSTLEND_TRON


class JustLendInfo:
    mapping = {
        Chain.tron: JUSTLEND_TRON
    }


class JustLendStateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x2b6653dc"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.justlend}"
        self.chain_id = chain_id
        self.pool_info = JustLendInfo.mapping.get(chain_id)

        # BASIC FUNCTIONS

    def get_service_info(self):
        info = {
            Lending.justlend: {
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
            ctokens.append(token)

        tokens = [Web3.toChecksumAddress(i) for i in ctokens]
        reserves_info = {}
        queries = {}
        for token in tokens:
            key = f"underlying_{token}_latest".lower()
            queries[key] = {
                "address": token,
                "abi": JUST_TOKEN_ABI,
                "params": [],
                "function": "underlying",
                "block_number": "latest"
            }
        decoded_data = self.state_service.query_state_data(queries)
        for token in tokens:
            key = f"underlying_{token}_latest".lower()
            underlying = decoded_data.get(key).lower()
            reserves_info[underlying] = {'cToken': token.lower()}
        return reserves_info

