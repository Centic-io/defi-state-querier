from defi_services.abis.dex.uniswap.factory_v2_abi import UNISWAP_FACTORY_ABI
from defi_services.abis.dex.uniswap.factory_v3_abi import UNISWAP_V3_FACTORY_ABI
from defi_services.abis.dex.uniswap.nft_token_manager_abi import UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI
from defi_services.abis.dex.uniswap.pool_v3_abi import UNISWAP_V3_POOL_ABI

UNISWAP_ETH_INFO = {
    'factory_address': '0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f',
    'factory_abi': UNISWAP_FACTORY_ABI
}

UNISWAP_V3_ETH_INFO = {
    'factory_address': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
    'factory_abi': UNISWAP_V3_FACTORY_ABI,
    'staker_address': '0xe34139463bA50bD61336E0c446Bd8C0867c6fE65',
    'NFT_manager_address': '0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
    'NFT_manager_abi': UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI,
    'pool_abi': UNISWAP_V3_POOL_ABI,
}
