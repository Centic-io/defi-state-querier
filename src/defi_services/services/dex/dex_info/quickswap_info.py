from defi_services.abis.dex.quickswap.factory_v3_abi import QUICKSWAP_V3_FACTORY_ABI
from defi_services.abis.dex.quickswap.nft_token_manager import QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.quickswap.pool_v3_abi import QUICKSWAP_V3_POOL_ABI

QUICKSWAP_POLYGON_V2_INFO = {
    'factory_address': '0x5757371414417b8c6caad45baef941abc7d3ab32',
    'forked': 'uniswap-v2'

}

QUICKSWAP_POLYGON_V3_INFO = {
    'factory_address': '0x411b0facc3489691f28ad58c47006af5e3ab3a28',
    'factory_abi': QUICKSWAP_V3_FACTORY_ABI,
    "NFT_manager_address": "0x8ef88e4c7cfbbac1c163f7eddd4b578792201de6",
    "NFT_manager_abi": QUICKSWAP_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI,
    'pool_abi':QUICKSWAP_V3_POOL_ABI,
    'finite_farming': '0x9923f42a02a82da63ee0dbbc5f8e311e3dd8a1f8',
    'infinite_farming': '0x8a26436e41d0b5fc4c6ed36c1976fafbe173444e',
    'farming_center': '0x7f281a8cdf66ef5e9db8434ec6d97acc1bc01e78',
    'forked': 'uniswap-v3'

}
