from defi_services.abis.dex.pancakeswap.masterchef_v3_abi import PANCAKESWAP_MASTERCHEF_V3_ABI
from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI

PANCAKESWAP_V0_BSC_INFO = {
    'masterchefAddress': '0x73feaa1ee314f8c655e354234017be2193c9e24e',
    "rewardToken": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"
}

PANCAKESWAP_V2_BSC_INFO = {
    'factoryAddress': '0xca143ce32fe78f1f7019d7d551a6402fc5350c73',
    'masterchefAddress': '0xa5f8c5dbd5f286960b9d90548680ae5ebff07652',
    "rewardToken": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"
}

PANCAKESWAP_V3_BSC_INFO = {
    'masterchefAddress': '0x556B9306565093C855AEA9AE92A594704c2Cd59e',
    'masterchef_abi': PANCAKESWAP_MASTERCHEF_V3_ABI,
    "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower(),
    "NFT_token_manager": "0x46A15B0b27311cedF172AB29E4f4766fbE7F4364".lower(),
    "NFT_abi": PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
}
