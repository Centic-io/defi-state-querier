import json

from defi_services.abis.lending.compound.comet.comet.comet import COMET
from defi_services.abis.lending.compound.comet.bridges.arbitrum_bridge_receiver import ARBITRUM_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.base_bridge_receiver import BASE_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.base_bridge_receiver_harness import BASE_BRIDGE_RECEIVER_HARNESS
from defi_services.abis.lending.compound.comet.bridges.linea_bridge_receiver import LINEA_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.optimism_bridge_receiver import OPTIMISM_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.polygon_bridge_receiver import POLYGON_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.sweepable_bridge_receiver import SWEEPABLE_BRIDGE_RECEIVER
from defi_services.abis.lending.compound.comet.bridges.sweepable_bridge_receiver_harness import \
    SWEEPABLE_BRIDGE_RECEIVER_HARNESS
from defi_services.abis.lending.compound.comet.bulkers.base_bulker import BASE_BULKER
from defi_services.abis.lending.compound.comet.bulkers.mainnet_bulker import MAINNET_BULKER
from defi_services.abis.lending.compound.comet.cometcore.comet_core import COMET_CORE
from defi_services.abis.lending.compound.comet.cometext.comet_ext import COMET_EXT
from defi_services.abis.lending.compound.comet.cometmaininterface.comet_main_interface import COMET_MAIN_INTERFACE
from defi_services.abis.lending.compound.comet.cometproxyadmin.comet_proxy_admin import COMET_PROXY_ADMIN
from defi_services.abis.lending.compound.comet.cometrewards.comet_rewards import COMET_REWARDS
from defi_services.abis.lending.compound.comet.configurator.configurator import CONFIGURATOR
from defi_services.abis.lending.compound.comet.configuratorproxy.configurator_proxy import CONFIGURATOR_PROXY
from defi_services.abis.lending.compound.comet.liquidator.on_chain_liquidator import ON_CHAIN_LIQUIDATOR
from defi_services.abis.lending.compound.compound_v3.comet_abi import COMET_ABI
from defi_services.abis.lending.compound.compound_v3.comet_ext_abi import COMET_EXT_ABI
from defi_services.abis.lending.compound.compound_v3.reward_abi import REWARD_ABI
from defi_services.abis.lending.compound.governance.comp import COMP
from defi_services.abis.lending.compound.governance.governor_bravo_delegate import GOVERNOR_BRAVO_DELEGATE
from defi_services.abis.lending.compound.governance.governor_bravo_delegator import GOVERNOR_BRAVO_DELEGATOR
from defi_services.abis.lending.compound.governance.timelock import TIMELOCK
from defi_services.abis.lending.compound.protocol.bravodelegate2 import BRAVODELEGATE2
from defi_services.abis.lending.compound.protocol.bravodelegator2 import BRAVODELEGATOR2
from defi_services.abis.lending.compound.protocol.comp import COMP_PROTOCOL
from defi_services.abis.lending.compound.protocol.compoundlens import COMPOUNDLENS
from defi_services.abis.lending.compound.protocol.comptroller import COMPTROLLER
from defi_services.abis.lending.compound.protocol.ctoken import CTOKEN
from defi_services.abis.lending.compound.protocol.dsr_updateable import DSR_UPDATEABLE
from defi_services.abis.lending.compound.protocol.governoralpha import GOVERNORALPHA
from defi_services.abis.lending.compound.protocol.governorbravo import GOVERNORBRAVO
from defi_services.abis.lending.compound.protocol.governorbravodelegator import GOVERNORBRAVODELEGATOR
from defi_services.abis.lending.compound.protocol.irm_comp_updateable import IRM_COMP_UPDATEABLE
from defi_services.abis.lending.compound.protocol.jumpratemodelv2 import JUMPRATEMODELV2
from defi_services.abis.lending.compound.protocol.legacyjumpratemodelv2 import LEGACYJUMPRATEMODELV2
from defi_services.abis.lending.compound.protocol.moneymarket import MONEYMARKET
from defi_services.abis.lending.compound.protocol.newbravodelegate import NEWBRAVODELEGATE
from defi_services.abis.lending.compound.protocol.newbravodelegator import NEWBRAVODELEGATOR
from defi_services.abis.lending.compound.protocol.pricedata import PRICEDATA
from defi_services.abis.lending.compound.protocol.pricefeed import PRICEFEED
from defi_services.abis.lending.compound.protocol.priceoracle import PRICEORACLE
from defi_services.abis.lending.compound.protocol.rep import REP
from defi_services.abis.lending.compound.protocol.reservoir import RESERVOIR
from defi_services.abis.lending.compound.protocol.stablecoininterestratemodel import STABLECOININTERESTRATEMODEL
from defi_services.abis.lending.compound.protocol.standardinterestratemodel import STANDARDINTERESTRATEMODEL
from defi_services.abis.lending.compound.protocol.stdcomptroller import STDCOMPTROLLER
from defi_services.abis.lending.compound.protocol.timelock import TIMELOCK_PROTOCOL
from defi_services.abis.lending.compound.protocol.uni import UNI
from defi_services.abis.lending.compound.protocol.unitroller import UNITROLLER


class CompoundABIs:
    mapping = [
        ARBITRUM_BRIDGE_RECEIVER,
        BASE_BRIDGE_RECEIVER,
        BASE_BRIDGE_RECEIVER_HARNESS,
        LINEA_BRIDGE_RECEIVER,
        OPTIMISM_BRIDGE_RECEIVER,
        POLYGON_BRIDGE_RECEIVER,
        SWEEPABLE_BRIDGE_RECEIVER,
        SWEEPABLE_BRIDGE_RECEIVER_HARNESS,
        BASE_BULKER,
        MAINNET_BULKER,
        COMET,
        COMET_CORE,
        COMET_EXT,
        COMET_MAIN_INTERFACE,
        COMET_PROXY_ADMIN,
        COMET_REWARDS,
        CONFIGURATOR,
        CONFIGURATOR_PROXY,
        ON_CHAIN_LIQUIDATOR,
        COMET_ABI,
        COMET_EXT_ABI,
        REWARD_ABI,
        COMP,
        GOVERNOR_BRAVO_DELEGATE,
        GOVERNOR_BRAVO_DELEGATOR,
        TIMELOCK,
        BRAVODELEGATE2,
        BRAVODELEGATOR2,
        COMP_PROTOCOL,
        COMPOUNDLENS,
        COMPTROLLER,
        CTOKEN,
        DSR_UPDATEABLE,
        GOVERNORALPHA,
        GOVERNORBRAVO,
        GOVERNORBRAVODELEGATOR,
        IRM_COMP_UPDATEABLE,
        JUMPRATEMODELV2,
        LEGACYJUMPRATEMODELV2,
        MONEYMARKET,
        NEWBRAVODELEGATE,
        NEWBRAVODELEGATOR,
        PRICEDATA,
        PRICEFEED,
        PRICEORACLE,
        REP,
        RESERVOIR,
        STABLECOININTERESTRATEMODEL,
        STANDARDINTERESTRATEMODEL,
        STDCOMPTROLLER,
        TIMELOCK_PROTOCOL,
        UNI,
        UNITROLLER
]

if __name__ == "__main__":
    result = []
    for i in CompoundABIs.mapping:
        for obj in i:
            if obj.get('type') == "event":
                if "signature" in obj:
                    del obj['signature']
                result.append(obj)
    with open("events.json", 'w') as f:
        json.dump(result, f, indent=2)