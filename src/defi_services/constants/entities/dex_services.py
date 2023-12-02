from src.defi_services.constants.chain_constant import Chain
from src.defi_services.constants.entities.dex_constant import Dex
from src.defi_services.services.dex.pancakeswap_service import PancakeswapServices
from src.defi_services.services.dex.sushiswap_service import SushiswapServices


# from src.defi_services.services.dex. import UniswapServices


class DexServices:
    ethereum = {
        # Dex.uniswap: UniswapServices,
        Dex.sushi: SushiswapServices
    }
    bsc = {
        Dex.pancake: PancakeswapServices,
        Dex.sushi: SushiswapServices
    }
    avalanche = {
        Dex.sushi: SushiswapServices

    }
    polygon = {
        Dex.sushi: SushiswapServices

    }
    fantom = {
        Dex.sushi: SushiswapServices

    }
    optimism = {
        Dex.sushi: SushiswapServices

    }
    arbitrum = {
        Dex.sushi: SushiswapServices

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
