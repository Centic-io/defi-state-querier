from defi_services.abis.dex.uniswap.factory_v2_abi import UNISWAP_FACTORY_ABI
from defi_services.abis.dex.uniswap.factory_v3_abi import UNISWAP_V3_FACTORY_ABI
from defi_services.abis.dex.uniswap.nft_token_manager_abi import UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI
from defi_services.abis.dex.uniswap.pool_v3_abi import UNISWAP_V3_POOL_ABI

UNISWAP_ETH_INFO = {
    'factory_address': '0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f',
    'factory_abi': UNISWAP_FACTORY_ABI,
    'forked': 'uniswap-v2'

}

UNISWAP_V3_ETH_INFO = {
    'factory_address': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
    'factory_abi': UNISWAP_V3_FACTORY_ABI,
    'staker_address': '0xe34139463bA50bD61336E0c446Bd8C0867c6fE65',
    'NFT_manager_address': '0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
    'NFT_manager_abi': UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI,
    'pool_abi': UNISWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3'
}


UNISWAP_V3_ARBITRUM_INFO = {
    'factory_address': '0x1f98431c8ad98523631ae4a59f267346ea31f984',
    'factory_abi': UNISWAP_V3_FACTORY_ABI,
    'staker_address': '0xe34139463ba50bd61336e0c446bd8c0867c6fe65',
    'NFT_manager_address': '0xc36442b4a4522e871399cd717abdd847ab11fe88',
    'NFT_manager_abi': UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI,
    'pool_abi': UNISWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3'
}

UNISWAP_V3_BASE_INFO = {
    'factory_address': '0x33128a8fC17869897dcE68Ed026d694621f6FDfD',
    'factory_abi': UNISWAP_V3_FACTORY_ABI,
    'staker_address': '0x42bE4D6527829FeFA1493e1fb9F3676d2425C3C1',
    'NFT_manager_address': '0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1',
    'NFT_manager_abi': UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI,
    'pool_abi': UNISWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3'
}

UNISWAP_V3_ZKSYNC_INFO = {
    'factory_address': '0x8FdA5a7a8dCA67BBcDd10F02Fa0649A937215422',
    'factory_abi': UNISWAP_V3_FACTORY_ABI,
    'staker_address': '0xf84268FA8EB857c2e4298720C1C617178F5e78e1',
    'NFT_manager_address': '0x0616e5762c1E7Dc3723c50663dF10a162D690a86',
    'NFT_manager_abi': UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI,
    'pool_abi': UNISWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3'
}
