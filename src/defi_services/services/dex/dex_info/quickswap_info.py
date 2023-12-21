from defi_services.abis.dex.quickswap.factory_v3_abi import QUICKSWAP_V3_FACTORY_ABI
from defi_services.abis.dex.quickswap.nft_token_manager import QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI

QUICKSWAP_POLYGON_V2_INFO = {
    'factoryAddress': '0x5757371414417b8c6caad45baef941abc7d3ab32',
}

QUICKSWAP_POLYGON_V3_INFO = {
    'factoryAddress': '0x411b0facc3489691f28ad58c47006af5e3ab3a28',
    'factory_abi': QUICKSWAP_V3_FACTORY_ABI,
    # "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower(),
    "NFT_token_manager": "0x8ef88e4c7cfbbac1c163f7eddd4b578792201de6",
    "NFT_abi": QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
}
