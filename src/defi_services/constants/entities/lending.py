from defi_services.constants.chain_constant import Chain
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.uwu_services import UwuStateService
from defi_services.services.lending.compound_service import CompoundStateService


class Lending:
    # service
    aave_v2 = "aave-v2"
    compound = "compound"
    uwu = "uwu"
    all = [uwu]

    # chain
    ethereum = {
        aave_v2: AaveV2StateService,
        compound: CompoundStateService,
        uwu: UwuStateService
    }

    # mapping
    mapping = {
        Chain.ethereum: ethereum
    }

