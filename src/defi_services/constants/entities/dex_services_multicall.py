from defi_services.services.dex.pancakeswap_v2_service_multicall import PancakeSwapV2Services
from defi_services.services.dex.pancakeswap_v3_service_multicall import PancakeSwapV3Service
from defi_services.services.dex.quickswap_v2_service import QuickSwapV2Services
from defi_services.services.dex.quickswap_v3_service_multicall import QuickSwapV3Services
from defi_services.services.dex.spookyswap_v2_service_multicall import SpookySwapV2Services
from defi_services.services.dex.sushiswap_v2_service_multicall import SushiSwapV2Services
from defi_services.services.dex.sushiswap_v3_service_multicall import SushiSwapV3Services
from defi_services.services.dex.uniswap_v2_service_multicall import UniswapV2Services
from defi_services.services.dex.uniswap_v3_service_multicall import UniswapV3Services

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.services.dex.pancakeswap_service_multicall import PancakeSwapServices
from defi_services.services.dex.sushiswap_service_multicall import SushiSwapServices


class DexServices:
    ethereum = {
        Dex.uniswap_v2: UniswapV2Services,
        Dex.uniswap_v3: UniswapV3Services,
        Dex.sushi: SushiSwapServices,
        Dex.sushi_v2: SushiSwapV2Services,
        Dex.sushi_v3: SushiSwapV3Services,

    }
    bsc = {
        Dex.pancake: PancakeSwapServices,
        Dex.pancake_v3: PancakeSwapV3Service,
        Dex.pancake_v2: PancakeSwapV2Services,
        Dex.sushi_v2: SushiSwapV2Services
    }
    avalanche = {
        Dex.sushi_v2: SushiSwapV2Services
    }
    polygon = {
        Dex.sushi_v2: SushiSwapV2Services,
        Dex.quickswap_v2: QuickSwapV2Services,
        Dex.quickswap_v3: QuickSwapV3Services
    }
    fantom = {
        Dex.sushi_v2: SushiSwapV2Services,
        Dex.spooky_v2: SpookySwapV2Services
    }
    # optimism = {
    #     Dex.sushi: SushiSwapV2Services
    # }
    arbitrum = {
        Dex.sushi_v2: SushiSwapV2Services
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
