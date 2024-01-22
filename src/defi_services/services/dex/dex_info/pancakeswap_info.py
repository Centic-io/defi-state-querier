from defi_services.abis.dex.pancakeswap.factory_v3_abi import PANCAKESWAP_V3_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.masterchef_v3_abi import PANCAKESWAP_MASTERCHEF_V3_ABI
from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_masterchef_v2_abi import PANCAKESWAP_MASTERCHEF_V2_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_v2_factory_abi import PANCAKESWAP_V2_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.v3_pool_abi import PANCAKESWAP_V3_POOL_ABI

PANCAKESWAP_V0_BSC_INFO = {
    'master_chef_address': '0x73feaa1ee314f8c655e354234017be2193c9e24e',
    "reward_token": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    'forked': 'uniswap-v2'

}

PANCAKESWAP_V2_BSC_INFO = {
    'factory_address': '0xca143ce32fe78f1f7019d7d551a6402fc5350c73',
    'master_chef_address': '0xa5f8c5dbd5f286960b9d90548680ae5ebff07652',
    "reward_token": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    'factory_abi': PANCAKESWAP_V2_FACTORY_ABI,
    'master_chef_abi': PANCAKESWAP_MASTERCHEF_V2_ABI,
    'forked': 'uniswap-v2'
}

PANCAKESWAP_V3_BSC_INFO = {
    'factory_address': '0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865',
    'factory_abi': PANCAKESWAP_V3_FACTORY_ABI,
    'master_chef_address': '0x556B9306565093C855AEA9AE92A594704c2Cd59e',
    'master_chef_abi': PANCAKESWAP_MASTERCHEF_V3_ABI,
    "reward_token": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower(),
    "NFT_manager_address": "0x46A15B0b27311cedF172AB29E4f4766fbE7F4364".lower(),
    "NFT_manager_abi": PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI,
    'pool_abi': PANCAKESWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3'

}
