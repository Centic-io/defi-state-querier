from defi_services.constants.chain_constant import Chain
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.geist_services import GeistStateService
from defi_services.services.lending.trava_services import TravaStateService
from defi_services.services.lending.valas_services import ValasStateService


class Lending:
    # service
    aave_v2 = "aave-v2"
    compound = "compound"
    trava = "trava"
    valas = "valas"
    geist = "geist"
    all = [aave_v2]

    # chain
    ethereum = {
        aave_v2: AaveV2StateService,
        compound: CompoundStateService,
        trava: TravaStateService
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

