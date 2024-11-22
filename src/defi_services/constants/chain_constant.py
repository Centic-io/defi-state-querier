class Chain:
    solana = "solana"
    bsc = "0x38"
    ethereum = "0x1"
    fantom = "0xfa"
    polygon = "0x89"
    arbitrum = "0xa4b1"
    optimism = "0xa"
    avalanche = "0xa86a"
    tron = "0x2b6653dc"
    cronos = "0x19"
    polkadot = "polkadot"
    base = '0x2105'
    kava = '0x8ae'
    gnosis = '0x64'
    klaytn = '0x2019'
    mantle = '0x1388'
    celo = '0xa4ec'
    moonbeam = '0x504'
    manta = '0xa9'
    pulse = '0x171'
    rootstock = '0x1e'
    astar = '0x250'
    metis = '0x440'
    canto = '0x1e14'
    heco = '0x80'
    linea = '0xe708'
    okc = '0x42'
    aurora = '0x4e454152'
    moonriver = '0x505'
    blast = '0xee'
    oasis_sapphire = '0x5afe'
    zeta = '0x1b58'

    native_decimals = {
        tron: 6,
        solana: 9,
        polkadot: 10
    }


class BlockTime:
    block_time_by_chains = {
        Chain.bsc: 3,
        Chain.ethereum: 12,
        Chain.fantom: 2,
        Chain.polygon: 2,
        Chain.arbitrum: 0.3,
        Chain.optimism: 1,  # TODO: check
        Chain.avalanche: 2,
        Chain.tron: 3,
        Chain.cronos: 6
    }
