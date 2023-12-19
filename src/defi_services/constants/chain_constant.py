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
