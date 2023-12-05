from defi_services.services.dex.pancakeswap_v2_service import PancakeSwapV2Info, PancakeSwapV2Services
from defi_services.services.dex.sushiswap_v2_service import SushiSwapV2Services
from src.defi_services.constants.chain_constant import Chain
from src.defi_services.constants.entities.dex_constant import Dex
from src.defi_services.services.dex.pancakeswap_service import PancakeswapServices
from src.defi_services.services.dex.sushiswap_service import SushiswapServices


# from src.defi_services.services.dex. import UniswapServices


class DexServices:
    ethereum = {
        # Dex.uniswap: UniswapServices,
        Dex.sushi: SushiswapServices,
        Dex.sushi_v2:SushiSwapV2Services
    }
    bsc = {
        Dex.pancake: PancakeswapServices,
        Dex.pancake_v2: PancakeSwapV2Services,
        Dex.sushi: SushiSwapV2Services
    }
    avalanche = {
        Dex.sushi: SushiSwapV2Services

    }
    polygon = {
        Dex.sushi: SushiSwapV2Services

    }
    fantom = {
        Dex.sushi: SushiSwapV2Services

    }
    optimism = {
        Dex.sushi: SushiSwapV2Services

    }
    arbitrum = {
        Dex.sushi: SushiSwapV2Services

    }
    mapping = {
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.bsc: bsc,
        Chain.avalanche: avalanche,
        Chain.polygon: polygon,
        Chain.arbitrum: arbitrum,
        Chain.optimism: optimism,
    }
