from defi_services.constants.chain_constant import Chain
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.aave_v3_services import AaveV3StateService
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.cream_services import CreamStateService
from defi_services.services.lending.geist_services import GeistStateService
from defi_services.services.lending.radiant_v2_services import RadiantStateService
from defi_services.services.lending.trava_services import TravaStateService
from defi_services.services.lending.valas_services import ValasStateService
from defi_services.services.lending.venus_services import VenusStateService
from defi_services.services.lending.onyx_service import OnyxStateService


class Lending:
    # service
    aave_v2 = "aave-v2"
    aave_v3 = "aave-v3"
    radiant_v2 = "radiant-v2"
    compound = "compound"
    trava = "trava-finance"
    valas = "valas-finance"
    geist = "geist-finance"
    cream = "cream-lending"
    venus = "venus"
    onyx = "onyx"
    all = [onyx]

    # chain
    ethereum = {
        aave_v2: AaveV2StateService,
        compound: CompoundStateService,
        trava: TravaStateService,
        aave_v3: AaveV3StateService,
        onyx: OnyxStateService
    }
    fantom = {
        trava: TravaStateService,
        geist: GeistStateService,
        aave_v3: AaveV3StateService,
    }

    bsc = {
        trava: TravaStateService,
        valas: ValasStateService,
        cream: CreamStateService,
        venus: VenusStateService,
        radiant_v2: RadiantStateService
    }

    avalanche = {
        aave_v3: AaveV3StateService,
        aave_v2: AaveV2StateService
    }

    polygon = {
        aave_v2: AaveV2StateService,
        aave_v3: AaveV3StateService
    }

    optimism = {
        aave_v3: AaveV3StateService
    }

    arbitrum = {
        radiant_v2: RadiantStateService,
        aave_v3: AaveV3StateService
    }
    # mapping
    mapping = {
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.bsc: bsc,
        Chain.avalanche: avalanche,
        Chain.polygon: polygon,
        Chain.arbitrum: arbitrum,
        Chain.optimism: optimism
    }

