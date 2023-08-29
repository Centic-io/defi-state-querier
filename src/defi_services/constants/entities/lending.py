from defi_services.constants.chain_constant import Chain
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.geist_services import GeistStateService
from defi_services.services.lending.trava_services import TravaStateService
from defi_services.services.lending.valas_services import ValasStateService
from defi_services.services.lending.iron_bank_service import IronBankStateService


class Lending:
    # service
    aave_v2 = "aave-v2"
    compound = "compound"
    trava = "trava"
    valas = "valas"
    geist = "geist"
    iron_bank = "iron_bank"
    all = [iron_bank]

    # chain
    ethereum = {
        aave_v2: AaveV2StateService,
        compound: CompoundStateService,
        trava: TravaStateService,
        iron_bank: IronBankStateService
    }
    fantom = {
        trava: TravaStateService,
        geist: GeistStateService
    }

    bsc = {
        trava: TravaStateService,
        valas: ValasStateService
    }
    # mapping
    mapping = {
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.bsc: bsc
    }

