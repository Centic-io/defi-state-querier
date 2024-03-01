from defi_services.abis.dex.pancakeswap.factory_v3_abi import PANCAKESWAP_V3_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.masterchef_v3_abi import PANCAKESWAP_MASTERCHEF_V3_ABI
from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_masterchef_v2_abi import PANCAKESWAP_MASTERCHEF_V2_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_v2_factory_abi import PANCAKESWAP_V2_FACTORY_ABI
from defi_services.abis.dex.pancakeswap.v3_pool_abi import PANCAKESWAP_V3_POOL_ABI

PANCAKESWAP_V0_BSC_INFO = {
    "project_id": "pancakeswap",
    "chain_id": "0x1",
    "router_address": "0xeff92a263d31888d860bd50809a8d171709b7b1c",
    'master_chef_address': '0x73feaa1ee314f8c655e354234017be2193c9e24e',
    "reward_token": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    'forked': 'uniswap-v2'

}

PANCAKESWAP_V2_BSC_INFO = {
    "project_id": "pancakeswap-amm",
    "chain_id": "0x38",
    'factory_address': '0xca143ce32fe78f1f7019d7d551a6402fc5350c73',
    'master_chef_address': '0xa5f8c5dbd5f286960b9d90548680ae5ebff07652',
    "reward_token": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    'factory_abi': PANCAKESWAP_V2_FACTORY_ABI,
    'master_chef_abi': PANCAKESWAP_MASTERCHEF_V2_ABI,
    'forked': 'uniswap-v2',
    "router_address": "0x10ed43c718714eb63d5aa57b78b54704e256024e",
}

PANCAKESWAP_V3_BSC_INFO = {
    "project_id": "pancakeswap-v3",
    "chain_id": "0x38",
    'factory_address': '0x0bfbcf9fa4f9c56b0f40a671ad40e0805a091865',
    'factory_abi': PANCAKESWAP_V3_FACTORY_ABI,
    'master_chef_address': '0x556b9306565093c855aea9ae92a594704c2cd59e',
    'master_chef_abi': PANCAKESWAP_MASTERCHEF_V3_ABI,
    "NFT_manager_address": "0x46a15b0b27311cedf172ab29e4f4766fbe7f4364",
    "NFT_manager_abi": PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI,
    'pool_abi': PANCAKESWAP_V3_POOL_ABI,
    'forked': 'uniswap-v3',
    "reward_token": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    'router_address': "0x13f4ea83d0bd40e75c8222255bc855a974568dd4"

}
