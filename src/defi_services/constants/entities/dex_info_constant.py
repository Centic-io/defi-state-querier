from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.services.dex.dex_info.pancakeswap_info import *
from defi_services.services.dex.dex_info.quickswap_info import QUICKSWAP_POLYGON_V2_INFO
from defi_services.services.dex.dex_info.spookyswap_info import SPOOKY_FTM_V2_INFO
from defi_services.services.dex.dex_info.sushiswap_info import *
from defi_services.services.dex.dex_info.uniswap_info import *


class DexInfo:
    ethereum = {
        Dex.uniswap_v2: UNISWAP_ETH_INFO,
        Dex.uniswap_v3: UNISWAP_V3_ETH_INFO,
        Dex.sushi: SUSHISWAP_V0_ETH_INFO,
        Dex.sushi_v2: SUSHISWAP_V2_ETH_INFO,

    }
    bsc = {
        Dex.pancake: PANCAKESWAP_V0_BSC_INFO,
        Dex.pancake_v3: PANCAKESWAP_V3_BSC_INFO,
        Dex.pancake_v2: PANCAKESWAP_V2_BSC_INFO,
        Dex.sushi_v2: SUSHISWAP_V2_BSC_INFO
    }
    avalanche = {
        Dex.sushi_v2: SUSHISWAP_V2_AVALANCHE_INFO
    }
    polygon = {
        Dex.sushi_v2: SUSHISWAP_V2_POLYGON_INFO,
        Dex.quickswap_v2: QUICKSWAP_POLYGON_V2_INFO
    }
    fantom = {
        Dex.sushi_v2: SUSHISWAP_V2_FANTOM_INFO,
        Dex.spooky_v2: SPOOKY_FTM_V2_INFO
    }
    # optimism = {
    #     Dex.sushi: SushiSwapV2Services
    # }
    arbitrum = {
        Dex.sushi_v2: SUSHISWAP_V2_ARBITRUM_INFO
    }
    mapping = {
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.bsc: bsc,
        Chain.avalanche: avalanche,
        Chain.polygon: polygon,
        Chain.arbitrum: arbitrum,
        # Chain.optimism: optimism,
    }

