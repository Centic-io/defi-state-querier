from defi_services.abis.dex.pancakeswap.masterchef_v0_abi import PANCAKESWAP_MASTERCHEF_V0_ABI
from defi_services.abis.dex.pancakeswap.masterchef_v3_abi import PANCAKESWAP_MASTERCHEF_V3_ABI
from defi_services.abis.dex.pancakeswap.nft_token_abi import PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_masterchef_v2_abi import PANCAKESWAP_MASTERCHEF_V2_ABI

PANCAKESWAP_V0_BSC_INFO = {
    'masterchef_address': '0x73feaa1ee314f8c655e354234017be2193c9e24e',
    'masterchef_abi': PANCAKESWAP_MASTERCHEF_V0_ABI,
    "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower()

    }

PANCAKESWAP_V2_BSC_INFO = {
    'masterchef_address': '0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652',
    'masterchef_abi': PANCAKESWAP_MASTERCHEF_V2_ABI,
    "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower()
}

PANCAKESWAP_V3_BSC_INFO={
'masterchef_address': '0x556B9306565093C855AEA9AE92A594704c2Cd59e',
    'masterchef_abi': PANCAKESWAP_MASTERCHEF_V3_ABI,
    "rewardToken": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82".lower(),
    "NFT_token_manager":"0x46A15B0b27311cedF172AB29E4f4766fbE7F4364".lower(),
    "NFT_abi": PANCAKE_V3_NON_FUNGIBLE_POSITION_TOKEN_ABI
    }
