from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.granary_v1_services import GranaryV1StateService
from defi_services.services.lending.uwu_services import UwuStateService
from defi_services.services.lending.aave_v3_services import AaveV3StateService
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.cream_services import CreamStateService
from defi_services.services.lending.geist_services import GeistStateService
from defi_services.services.lending.radiant_v2_services import RadiantStateService
from defi_services.services.lending.trava_services import TravaStateService
from defi_services.services.lending.valas_services import ValasStateService
from defi_services.services.lending.flux_services import FluxStateService
from defi_services.services.lending.iron_bank_service import IronBankStateService
from defi_services.services.lending.venus_services import VenusStateService
from defi_services.services.lending.liqee_service import LiqeeStateService
from defi_services.services.lending.strike_service import StrikeStateService
from defi_services.services.lending.onyx_service import OnyxStateService
from defi_services.services.lending.wepiggy_services import WepiggyStateService


class LendingServices:
    # chain
    ethereum = {
        Lending.aave_v2: AaveV2StateService,
        Lending.compound: CompoundStateService,
        Lending.trava: TravaStateService,
        Lending.flux: FluxStateService,
        Lending.iron_bank: IronBankStateService,
        Lending.uwu: UwuStateService,
        Lending.aave_v3: AaveV3StateService,
        Lending.liqee: LiqeeStateService,
        Lending.strike: StrikeStateService,
        Lending.onyx: OnyxStateService,
        Lending.granary: GranaryV1StateService,
        Lending.wepiggy: WepiggyStateService
    }
    fantom = {
        Lending.trava: TravaStateService,
        Lending.geist: GeistStateService,
        Lending.aave_v3: AaveV3StateService,
    }

    bsc = {
        Lending.trava: TravaStateService,
        Lending.valas: ValasStateService,
        Lending.cream: CreamStateService,
        Lending.venus: VenusStateService,
        Lending.radiant_v2: RadiantStateService
    }

    avalanche = {
        Lending.aave_v3: AaveV3StateService,
        Lending.aave_v2: AaveV2StateService
    }

    polygon = {
        Lending.aave_v2: AaveV2StateService,
        Lending.aave_v3: AaveV3StateService
    }

    optimism = {
        Lending.aave_v3: AaveV3StateService
    }

    arbitrum = {
        Lending.radiant_v2: RadiantStateService,
        Lending.aave_v3: AaveV3StateService
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
