
from defi_services.abis.dex.quickswap.factory_v3_abi import QUICKSWAP_V3_FACTORY_ABI
from defi_services.abis.dex.quickswap.nft_token_manager import QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.uniswap.uniswap_v2_factory import UNISWAP_FACTORY_ABI

QUICKSWAP_POLYGON_V2_INFO= {
    'factory_address': '0x5757371414417b8c6caad45baef941abc7d3ab32',
    'factory_abi': UNISWAP_FACTORY_ABI,
}

QUICKSWAP_POLYGON_V3_INFO = {
    'factory_address': '0x411b0fAcC3489691f28ad58c47006AF5E3Ab3A28',
    'factory_abi': QUICKSWAP_V3_FACTORY_ABI ,
    # "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower(),
    "NFT_token_manager":"0x8eF88E4c7CfbbaC1C163f7eddd4B578792201de6".lower(),
    "NFT_abi": QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
    }