import os

import dotenv

dotenv.load_dotenv()

POLYGON_AAVE_ADDRESS = '0x8dff5e27ea6b7ac08ebfdf9eb090f32ee9a30fcf'
ETHEREUM_AAVE_ADDRESS = '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9'

BSC_TRAVA_ADDRESS = '0x75de5f7c91a89c16714017c7443eca20c7a8c295'
ETH_TRAVA_ADDRESS = '0xd61afaaa8a69ba541bc4db9c9b40d4142b43b9a4'
FTM_TRAVA_ADDRESS = '0xd98bb590bdfabf18c164056c185fbb6be5ee643f'

BSC_VALAS_ADDRESS = '0xe29a55a6aeff5c8b1beede5bcf2f0cb3af8f91f5'

BSC_VENUS_ADDRESS = '0xfd36e2c2a6789db23113685031d7f16329158384'
BSC_CREAM_ADDRESS = '0x589de0f0ccf905477646599bb3e5c622c84cc0ba'

FTM_GEIST_ADDRESS = '0x9fad24f572045c7869117160a571b2e50b10d068'

ETH_COMPOUND_ADDRESS = '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b'
ETH_CREAM_ADDRESS = ''


class Chains:
    bsc = '0x38'
    ethereum = '0x1'
    fantom = '0xfa'
    polygon = '0x89'
    arbitrum = '0xa4b1'
    optimism = '0xa'
    avalanche = '0xa86a'
    tron = '0x2b6653dc'
    cronos = '0x19'
    solana = 'solana'
    polkadot = 'polkadot'
    bitcoin = 'bitcoin'
    cosmos = 'cosmos'
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
    oasis_sapphire = '0x5afe'
    oasis_sapphire_testnet = '0x5aff'
    blast = '0xee'
    oraichain = 'orai'
    ton = 'ton'

    none_wrapped_token = [arbitrum, fantom, optimism]
    all = [
        bsc, ethereum, fantom, polygon, arbitrum, optimism,
        avalanche, tron, cronos, solana, polkadot, bitcoin, cosmos,
        oraichain, ton
    ]

    mapping = {
        'bsc': bsc,
        'ethereum': ethereum,
        'fantom': fantom,
        'polygon': polygon,
        'arbitrum': arbitrum,
        'optimism': optimism,
        'avalanche': avalanche,
        'tron': tron,
        'cronos': cronos,
        'solana': solana,
        'polkadot': polkadot,
        'oasis_sapphire': oasis_sapphire,
        'oasis_sapphire_testnet': oasis_sapphire_testnet,
        'ton': ton
    }

    names = {
        bsc: 'bsc',
        ethereum: "ethereum",
        fantom: 'fantom',
        polygon: 'polygon',
        arbitrum: 'arbitrum',
        optimism: 'optimism',
        avalanche: 'avalanche',
        tron: 'tron',
        cronos: 'cronos',
        solana: 'solana',
        polkadot: 'polkadot',
        oasis_sapphire: 'oasis_sapphire',
        oasis_sapphire_testnet: 'oasis_sapphire_testnet',
        ton: 'ton'
    }

    abi_mapping = {
        bsc: 'bep20_abi',
        ethereum: 'erc20_abi',
        fantom: 'erc20_abi',
        polygon: 'erc20_abi',
        arbitrum: 'erc20_abi',
        optimism: 'erc20_abi',
        avalanche: 'erc20_abi',
        tron: 'trc20_abi',
        cronos: 'crc20_abi'
    }

    block_time = {
        bsc: 3,
        ethereum: 12,
        fantom: 1,
        polygon: 2,
        arbitrum: 0.3,
        avalanche: 2,
        ton: 3
    }
    wrapped_native_token = {
        bsc: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
        ethereum: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        polygon: "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
        fantom: "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
        arbitrum: "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
        optimism: "0x4200000000000000000000000000000000000006",
        avalanche: "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
        tron: "0x891cdb91d149f23b1a45d9c5ca78a88d0cb44c18",
        cronos: "0x5c7f8a570d578ed84e63fdfa7b1ee72deae1ae23",
    }

    evm = {
        ethereum: True, bsc: True, polygon: True, fantom: True,
        arbitrum: True, optimism: True, avalanche: True, tron: True, cronos: True,
        base: True, kava: True, gnosis: True, klaytn: True, mantle: True, celo: True, moonbeam: True, manta: True,
        pulse: True, rootstock: True, astar: True, metis: True, canto: True, heco: True, linea: True, okc: True,
        aurora: True, moonriver: True, oasis_sapphire: True, blast: True
    }

    def get_abi_name(self, chain_id):
        """Map chain_id with the corresponding abi key
        e.g.: '0x38' -> 'bep20_abi' or '0x1' -> 'erc20_abi'
        """
        return self.abi_mapping.get(chain_id, '')


class ChainsAnkr:
    """Chain name for Ankr API"""
    bsc = '0x38'
    eth = '0x1'
    fantom = '0xfa'
    polygon = '0x89'

    reversed_mapping = {
        bsc: 'bsc',
        eth: 'eth',
        fantom: 'fantom',
        polygon: 'polygon',
    }

    def get_chain_name(self, chain_id):
        return self.reversed_mapping.get(chain_id)


class Scans:
    mapping = {
        'bscscan': Chains.bsc,
        'etherscan': Chains.ethereum,
        'ftmscan': Chains.fantom,
        'polygonscan': Chains.polygon,
        'arbiscan': Chains.arbitrum,
        'optimistic': Chains.optimism,
        'snowtrace': Chains.avalanche,
        'cronoscan': Chains.cronos
    }

    api_keys = {
        Chains.bsc: 'GKRVTEQHSGWX335P21994DKNSTJVDYYXJ1',
        Chains.ethereum: 'YQVXQAJAYNS7AC48ZXS1NT45RKYRPY7P7E',
        Chains.fantom: 'Y85XY5DDDN4Z7C7Z4ZX8N62M5WET7D8NYC',
        Chains.polygon: 'EYADI5Q4VK4VF99KFEJURMVE9CNE54YEYW',
        Chains.arbitrum: 'BU5VN8872FE119RDX898MS5EZHE11FPZSC',
        Chains.optimism: '1JW9PDV2HZZI3WRFQRVGWUDD2T1RV8GWX3',
        Chains.avalanche: 'JWNM6Y5UA1499PWVA2T55MEH3TZDGAKJWJ',
        Chains.cronos: 'F5J6423D42PM21CDP61SUD6H7DE4FXH2DE'
    }

    api_bases = {
        Chains.bsc: 'https://api.bscscan.com/api',
        Chains.ethereum: 'https://api.etherscan.io/api',
        Chains.fantom: 'https://api.ftmscan.com/api',
        Chains.polygon: 'https://api.polygonscan.com/api',
        Chains.arbitrum: 'https://api.arbiscan.io/api',
        Chains.optimism: 'https://api-optimistic.etherscan.io/api',
        Chains.avalanche: 'https://api.snowtrace.io/api',
        Chains.cronos: 'https://cronoscan.com/api',
        Chains.ton: 'https://toncenter.com/api/'
    }

    scan_base_urls = {
        Chains.ethereum: 'https://etherscan.io/',
        Chains.bsc: 'https://bscscan.com/',
        Chains.fantom: 'https://ftmscan.com/',
        Chains.polygon: 'https://polygonscan.com/',
        Chains.arbitrum: 'https://arbiscan.io/',
        Chains.optimism: 'https://optimistic.etherscan.io/',
        Chains.avalanche: 'https://snowtrace.io/',
        Chains.cronos: 'https://cronoscan.com/',
        Chains.ton: 'https://toncenter.com/api/'
    }

    all_base_urls = {
        Chains.bsc: [
            'https://bscscan.com/token',
            'https://bscscan-com.translate.goog/token'
        ],
        Chains.polygon: [
            'https://polygonscan.com/token',
            'https://polygonscan-com.translate.goog/token'
        ],
        Chains.ethereum: [
            'https://etherscan.io/token',
            'https://etherscan-io.translate.goog/token',
        ],
        Chains.fantom: [
            'https://ftmscan.com/token',
            'https://ftmscan-com.translate.goog/token'
        ],
        Chains.arbitrum: [
            # 'https://arbiscan-io.translate.goog/token',
            'https://arbiscan.io/token'
        ],
        Chains.optimism: [
            # 'https://optimistic-etherscan-io.translate.goog/token',
            'https://optimistic.etherscan.io/token'
        ],
        # Chains.avalanche: [
        #     'https://snowtrace.io/token'
        # ],
        Chains.cronos: ['https://cronoscan.com/token']
    }

    gg_translate_suffix = '?_x_tr_sl=vi&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp'


class Networks:
    bsc = 'bsc'
    ethereum = 'ethereum'
    fantom = 'fantom'
    polygon = 'polygon'
    arbitrum = 'arbitrum'
    optimism = 'optimism'
    avalanche = 'avalanche'
    tron = 'tron'
    cronos = 'cronos'
    solana = 'solana'
    polkadot = 'polkadot'
    oasis_sapphire = 'oasis_sapphire'
    oasis_sapphire_testnet = 'oasis_sapphire_testnet'
    cosmos = 'cosmos'
    oraichain = 'oraichain'
    ton = 'ton'

    providers = {
        bsc: os.getenv('BSC_PROVIDER_URI', 'https://bsc-dataseed1.binance.org/'),
        ethereum: os.getenv('ETHEREUM_PROVIDER_URI', 'https://rpc.ankr.com/eth'),
        fantom: os.getenv('FANTOM_PROVIDER_URI', 'https://rpc.ftm.tools/'),
        polygon: os.getenv('POLYGON_PROVIDER_URI', 'https://polygon-rpc.com'),
        arbitrum: os.getenv('ARBITRUM_PROVIDER_URI', 'https://endpoints.omniatech.io/v1/arbitrum/one/public'),
        optimism: os.getenv('OPTIMISM_PROVIDER_URI', 'https://rpc.ankr.com/optimism'),
        avalanche: os.getenv('AVALANCHE_PROVIDER_URI', 'https://rpc.ankr.com/avalanche'),
        tron: os.getenv('TRON_PROVIDER_URI', 'https://rpc.ankr.com/tron_jsonrpc'),
        cronos: os.getenv('CRONOS_PROVIDER_URI', 'https://evm.cronos.org/'),
        solana: os.getenv('SOLANA_PROVIDER_URI', 'https://crimson-multi-putty.solana-mainnet.quiknode.pro/997174ce6ab5cc9d42cb037e931d18ae1a98346a/'),
        polkadot: os.getenv('POLKADOT_PROVIDER_URI', 'https://late-yolo-diagram.dot-mainnet.quiknode.pro/51a1aaf2372854dfd211fca3ab375e5451222be4/'),
        oasis_sapphire: os.getenv('OASIS_SAPPHIRE_PROVIDER_URI'),
        oasis_sapphire_testnet: os.getenv('OASIS_SAPPHIRE_PROVIDER_URI'),
        ton: os.getenv('TON_PROVIDER_URI')
    }

    archive_node = {
        bsc: os.getenv('BSC_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/bsc'),
        ethereum: os.getenv('ETHEREUM_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/eth'),
        fantom: os.getenv('FANTOM_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/fantom'),
        polygon: os.getenv('POLYGON_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/polygon'),
        arbitrum: os.getenv('ARBITRUM_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/arbitrum'),
        optimism: os.getenv('OPTIMISM_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/optimism'),
        avalanche: os.getenv('AVALANCHE_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/avalanche'),
        tron: os.getenv('TRON_PROVIDER_ARCHIVE_URI', 'https://rpc.ankr.com/tron_jsonrpc'),
        cronos: os.getenv('CRONOS_PROVIDER_ARCHIVE_URI'),
        solana: os.getenv('SOLANA_PROVIDER_ARCHIVE_URI'),
        polkadot: os.getenv('POLKADOT_PROVIDER_ARCHIVE_URI'),
        oasis_sapphire: os.getenv('OASIS_SAPPHIRE_PROVIDER_ARCHIVE_URI'),
        oasis_sapphire_testnet: os.getenv('OASIS_SAPPHIRE_PROVIDER_ARCHIVE_URI'),
        ton: os.getenv('TON_PROVIDER_ARCHIVE_URI', 'https://toncenter.com/api/')
    }


class DefiLlama:
    chains = {
        'Binance': Chains.bsc,
        'Ethereum': Chains.ethereum,
        'Fantom': Chains.fantom,
        'Polygon': Chains.polygon,
        'Arbitrum': Chains.arbitrum,
        'Optimism': Chains.optimism,
        'Avalanche': Chains.avalanche,
        'Tron': Chains.tron,
        'Cronos': Chains.cronos,
        'Solana': Chains.solana,
        'Polkadot': Chains.polkadot,
        'Base': Chains.base,
        'Kava': Chains.kava,
        'xDai': Chains.gnosis,
        'Klaytn': Chains.klaytn,
        'Mantle': Chains.mantle,
        'Celo': Chains.celo,
        'Moonbeam': Chains.moonbeam,
        'Manta': Chains.manta,
        'Pulse': Chains.pulse,
        'RSK': Chains.rootstock,
        'Astar': Chains.astar,
        'Metis': Chains.metis,
        'Canto': Chains.canto,
        'Heco': Chains.heco,
        'Linea': Chains.linea,
        'OKExChain': Chains.okc,
        'Aurora': Chains.aurora,
        'Moonriver': Chains.moonriver,
        'Oasis Sapphire': Chains.oasis_sapphire,
        'Blast': Chains.blast,
        'Oraichain': Chains.oraichain,
        'Ton': Chains.ton
    }


class Opensea:
    chains = {
        Chains.bsc: 'BSC',
        Chains.ethereum: 'ETHEREUM',
        Chains.polygon: 'MATIC',
        Chains.fantom: 'FANTOM',
        Chains.arbitrum: 'ARBITRUM',
        Chains.optimism: 'OPTIMISM',
        Chains.avalanche: 'AVALANCHE',
        Chains.tron: 'TRON',
        Chains.solana: 'SOLANA',
        Chains.base: 'BASE',
        Chains.klaytn: 'KLAYTN',
        Chains.ton: 'TON'
    }


NATIVE_TOKEN = '0x0000000000000000000000000000000000000000'

NATIVE_TOKENS = {
    Chains.bsc: '0x0000000000000000000000000000000000000000',
    Chains.ethereum: '0x0000000000000000000000000000000000000000',
    Chains.fantom: '0x0000000000000000000000000000000000000000',
    Chains.polygon: '0x0000000000000000000000000000000000000000',
    Chains.arbitrum: '0x0000000000000000000000000000000000000000',
    Chains.optimism: '0x0000000000000000000000000000000000000000',
    Chains.avalanche: '0x0000000000000000000000000000000000000000',
    Chains.tron: '0x0000000000000000000000000000000000000000',
    Chains.ton: 'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'
}


class MulticallContract:
    """
    References: https://www.multicall3.com/deployments
    """

    on_chains_v3 = {
        Chains.ethereum: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.bsc: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.polygon: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.avalanche: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.fantom: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.arbitrum: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.optimism: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.tron: '0x32a4f47a74a6810bd0bf861cabab99656a75de9e',
        Chains.oasis_sapphire: '0xca11bde05977b3631167028862be2a173976ca11',
        Chains.oasis_sapphire_testnet: '0xca11bde05977b3631167028862be2a173976ca11'
    }

    default_address = '0xca11bde05977b3631167028862be2a173976ca11'

    @classmethod
    def get_multicall_contract(cls, chain_id):
        return cls.on_chains_v3.get(chain_id, cls.default_address)


EMPTY_TOKEN_IMG = 'https://firebasestorage.googleapis.com/v0/b/token-c515a.appspot.com/o/tokens_v2%2Fempty-token.png?alt=media&token=2f9dfcc1-88a0-472c-a51f-4babc0c583f0'
