from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending


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
    wrapped_cro = '0x5c7f8a570d578ed84e63fdfa7b1ee72deae1ae23'

    wrapped_token = {
        Chain.solana: wrapped_sol,
        Chain.ethereum: wrapped_ethereum,
        Chain.bsc: wrapped_bsc,
        Chain.fantom: wrapped_ftm,
        Chain.avalanche: wrapped_avax,
        Chain.optimism: wrapped_eth_optimism,
        Chain.arbitrum: wrapped_eth_arbitrum,
        Chain.polygon: wrapped_matic,
        Chain.tron: wrapped_tron,
        Chain.cronos: wrapped_cro,
        Chain.base: '0x4200000000000000000000000000000000000006',
        Chain.kava: '0xc86c7c0efbd6a49b35e8714c5f59d99de09a225b',
        Chain.gnosis: '0xe91d153e0b41518a2ce8dd3d7944fa863463a97d',
        Chain.klaytn: '0x19aac5f612f524b754ca7e7c41cbfa2e981a4432',
        Chain.mantle: '0x78c1b0c915c4faa5fffa6cabf0219da63d7f4cb8',
        Chain.celo: '0x3ad443d769a07f287806874f8e5405ce3ac902b9',
        Chain.moonbeam: '0xacc15dc74880c9944775448304b263d191c6077f',
        Chain.manta: '0x0dc808adce2099a9f62aa87d9670745aba741746',
        Chain.pulse: '0xa1077a294dde1b09bb078844df40758a5d0f9a27',
        Chain.rootstock: '0x967f8799af07df1534d48a95a5c9febe92c53ae0',
        Chain.astar: '0xaeaaf0e2c81af264101b9129c00f4440ccf0f720',
        Chain.metis: '0x75cb093e4d61d2a2e65d8e0bbb01de8d89b53481',
        Chain.canto: '0x826551890dc65655a0aceca109ab11abdbd7a07b',
        Chain.heco: '0x5545153ccfca01fbd7dd11c0b23ba694d9509a6f',
        Chain.linea: '0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f',
        Chain.okc: '0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15',
        Chain.aurora: '0xc9bdeed33cd01541e1eed10f90519d2c06fe3feb',
        Chain.moonriver: '0x98878b06940ae243284ca214f92bb71a2b032b8a',
        Chain.blast: '0x4300000000000000000000000000000000000004',
        Chain.oasis_sapphire: '0x8bc2b030b299964eefb5e1e0b36991352e56d2d3'
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
    PANCAKE_FARM_V2 = "0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652"
    SUSHISWAP_FARM = "0xc2edad668740f1aa35e4d8f227fb8e17dca888cd"
    SUSHISWAP_FARM_V2 = '0xef0881ec094552b2e128cf945ef17a6752b4ec5d'
    MINICHEF_ARBITRUM_NOVA = '0xC09756432dAD2FF50B2D40618f7B04546DD20043'
    MINICHEF_ARBITRUM_ONE = '0xF4d73326C13a4Fc5FD7A064217e12780e9Bd62c3'
    MINICHEF_AVALANCHE = '0xe11252176CEDd4a493Aec9767192C06A04A6B04F'
    MINICHEF_BSC = '0x5219C5E32b9FFf87F29d5A833832c29134464aaa'
    MINICHEF_FANTOM = "0xf731202A3cf7EfA9368C2d7bD613926f7A144dB5"
    MINICHEF_OPTIMISM = '0xB25157bF349295a7Cd31D1751973f426182070D6'
    MINICHEF_POLYGON = '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F'
    SUSHISWAP_MINICHEF = {
        Chain.bsc: MINICHEF_BSC,
        Chain.fantom: MINICHEF_FANTOM,
        Chain.polygon: MINICHEF_POLYGON,
        Chain.optimism: MINICHEF_OPTIMISM,
        Chain.avalanche: MINICHEF_AVALANCHE,
    }


class ProtocolNFT:
    nft = {
        "0x60e4d786628fea6478f785a6d7e704777c86a7c6": Lending.onyx,
        "0xb7f7f6c52f2e2fdb1963eab30438024864c313f6": Lending.onyx,
        "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d": Lending.onyx
    }
