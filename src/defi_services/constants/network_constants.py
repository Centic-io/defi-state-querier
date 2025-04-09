
from defi_services.constants.chain_constant import Chain

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

NATIVE_TOKEN = '0x0000000000000000000000000000000000000000'

NATIVE_TOKENS = {
    Chain.bsc: '0x0000000000000000000000000000000000000000',
    Chain.ethereum: '0x0000000000000000000000000000000000000000',
    Chain.fantom: '0x0000000000000000000000000000000000000000',
    Chain.polygon: '0x0000000000000000000000000000000000000000',
    Chain.arbitrum: '0x0000000000000000000000000000000000000000',
    Chain.optimism: '0x0000000000000000000000000000000000000000',
    Chain.avalanche: '0x0000000000000000000000000000000000000000',
    Chain.tron: '0x0000000000000000000000000000000000000000',
    Chain.ton: 'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'
}


class MulticallContract:
    """
    References: https://www.multicall3.com/deployments
    """

    on_chains_v3 = {
        Chain.ethereum: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.bsc: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.polygon: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.avalanche: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.fantom: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.arbitrum: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.optimism: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.tron: '0x32a4f47a74a6810bd0bf861cabab99656a75de9e',
        Chain.oasis_sapphire: '0xca11bde05977b3631167028862be2a173976ca11',
        Chain.zksync: '0xf9cda624fbc7e059355ce98a31693d299facd963'
    }

    default_address = '0xca11bde05977b3631167028862be2a173976ca11'

    @classmethod
    def get_multicall_contract(cls, chain_id):
        return cls.on_chains_v3.get(chain_id, cls.default_address)
