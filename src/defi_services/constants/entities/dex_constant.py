from defi_services.constants.chain_constant import Chain
from defi_services.services.dex.dex_info.pancakeswap_info import *
from defi_services.services.dex.dex_info.sushiswap_info import *


class Dex:
    pancake = 'pancakeswap'

    pancake_v2 = 'pancakeswap-amm'
    pancake_v3 = 'pancakeswap-v3'
    sushi = 'sushi'
    sushi_v2 = 'sushiswap'
    sushi_v3 = 'sushiswap-v3'
    uniswap_v2 = 'uniswap-v2'
    uniswap_v3 = 'uniswap-v3'
    spooky_v2 = 'spookyswap'
    quickswap_v2 = 'quickswap-dex'
    quickswap_v3 = 'quickswap-v3'

class DexInfo:
    Dex.pancake = {
        Chain.bsc: PANCAKESWAP_V0_BSC_INFO}
    Dex.pancake_v2={
        Chain.bsc:PANCAKESWAP_V2_BSC_INFO}
    Dex.pancake_v3={Chain.bsc: PANCAKESWAP_V3_BSC_INFO}
    Dex.sushi= {
        Chain.ethereum: SUSHISWAP_V0_ETH_INFO
    }
    Dex.sushi_v2= {
        Chain.ethereum:SUSHISWAP_V2_ETH_INFO,
        Chain.bsc: SUSHISWAP_V2_BSC_INFO,
        Chain.fantom: SUSHISWAP_V2_FANTOM_INFO,
        Chain.polygon: SUSHISWAP_V2_POLYGON_INFO,
        Chain.avalanche: SUSHISWAP_V2_AVALANCHE_INFO,
        Chain.arbitrum:SUSHISWAP_V2_ARBITRUM_INFO
    }
    Dex.sushi_v3= {
        Chain.ethereum: SUSHISWAP_V3_ETH_INFO
    }
