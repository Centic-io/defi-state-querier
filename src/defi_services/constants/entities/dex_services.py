from defi_services.services.dex.pancakeswap_v2_service import PancakeSwapV2Services
from defi_services.services.dex.pancakeswap_v3_service import PancakeSwapV3Service
from defi_services.services.dex.quickswap_v2_service import QuickSwapV2Services
from defi_services.services.dex.quickswap_v3_service import QuickSwapV3Services
from defi_services.services.dex.spookyswap_v2_service import SpookySwapV2Services
from defi_services.services.dex.sushiswap_v2_service import SushiSwapV2Services
from defi_services.services.dex.sushiswap_v3_service import SushiSwapV3Services
from defi_services.services.dex.uniswap_v2_service import UniswapV2Services
from defi_services.services.dex.uniswap_v3_service import UniswapV3Services

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.services.dex.pancakeswap_service import PancakeSwapServices
from defi_services.services.dex.sushiswap_service import SushiSwapServices


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
        Dex.sushi_v2: SushiSwapV2Services,
        Dex.uniswap_v3: UniswapV3Services
    }

    zksync = {
        Dex.uniswap_v3: UniswapV3Services
    }

    base = {
        Dex.uniswap_v3: UniswapV3Services
    }

    mapping = {
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.bsc: bsc,
        Chain.avalanche: avalanche,
        Chain.polygon: polygon,
        Chain.arbitrum: arbitrum,
        # Chain.optimism: optimism,
        Chain.zksync: zksync,
        Chain.base: base
    }
