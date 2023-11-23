from defi_services.constants.chain_constant import Chain


class Token:
    native_token = '0x0000000000000000000000000000000000000000'
    wrapped_ethereum = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    wrapped_bsc = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
    wrapped_ftm = '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83'
    wrapped_avax = "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7"
    wrapped_eth_optimism = "0x4200000000000000000000000000000000000006"
    wrapped_eth_arbitrum = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
    wrapped_matic = '0x0000000000000000000000000000000000001010'
    wrapped_sol = 'So11111111111111111111111111111111111111112'
    wrapped_tron = '0x891cdb91d149f23b1a45d9c5ca78a88d0cb44c18'
    wrapped_token = {
        Chain.solana: wrapped_sol,
        Chain.ethereum: wrapped_ethereum,
        Chain.bsc: wrapped_bsc,
        Chain.fantom: wrapped_ftm,
        Chain.avalanche: wrapped_avax,
        Chain.optimism: wrapped_eth_optimism,
        Chain.arbitrum: wrapped_eth_arbitrum,
        Chain.polygon: wrapped_matic,
        Chain.tron: wrapped_tron
    }


class ContractAddresses:
    WBNB = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    BNB = "0x0000000000000000000000000000000000000000"
    TRAVA_BNB_LP = "0x865c77d4ff6383e06c58350a2cfb95cca2c0f056"
    R_TRAVA = "0x170772a06affc0d375ce90ef59c8ec04c7ebf5d2"
    VE_TRAVA_VAULT = "0xedf6a93772eecfb1300f61f6c1ae9680c33996a2"
    GENERAL_TRAVA_VAULT = "63daeb1c97e098480b16c7410dc4b9c0d4c401d6ff4735324edfbeaa"
    PANCAKE_FARM = "0x73feaa1ee314f8c655e354234017be2193c9e24e"
    # PANCAKE_FARM = "0xa5f8c5dbd5f286960b9d90548680ae5ebff07652"
    TRAVA_BSC_LENDING_POOL = "0x75de5f7c91a89c16714017c7443eca20c7a8c295"
    VALAS_BSC_LENDING_POOL = "0xe29a55a6aeff5c8b1beede5bcf2f0cb3af8f91f5"
    ALPACA_BSC_LENDING_POOL = "0xa625ab01b08ce023b2a342dbb12a16f2c8489a8f"
    DOGE = "0xba2ae424d960c26247dd6c32edc70b295c744c43"
    MAIN_STAKING_CONTRACT_PANCAKE_FARM = "0x73feaa1ee314f8c655e354234017be2193c9e24e"
    # MAIN_STAKING_CONTRACT_PANCAKE_FARM = "0xa5f8c5dbd5f286960b9d90548680ae5ebff07652"
    LUNA = "0xb91A659E88B51474767CD97EF3196A3e7cEDD2c8"
    UST = "0x78366446547D062f45b4C0f320cDaa6d710D87bb"
    BISWAP_FARM = "0xdbc1a13490deef9c3c12b44fe77b503c1b061739"
    PANCAKE_FARM_V2= "0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652"
