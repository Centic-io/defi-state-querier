import logging

from defi_services.constants.chain_constant import Chain
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.sushiswap_info import SUSHISWAP_V3_ETH_INFO
from defi_services.services.dex.uniswap_v3_service import UniswapV3Services

logger = logging.getLogger("SushiSwap V3 State Service")


class SushiSwapV3Info:
    mapping = {
        Chain.ethereum: SUSHISWAP_V3_ETH_INFO
    }


class SushiSwapV3Services(UniswapV3Services):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__(state_service, chain_id)
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = SushiSwapV3Info.mapping.get(chain_id)
        self.web3 = self.state_service.get_w3()
        if self.pool_info is not None:
            self.factory_abi = self.pool_info.get('factory_abi')
            self.nft_token_manager_addr = self.pool_info.get('NFT_manager_address')
            self.nft_token_manager_abi = self.pool_info.get('NFT_manager_abi')
            self.factory_addr = self.pool_info.get('factory_address')

    def get_all_supported_lp_token(self, limit: int = 100, supplied_data: dict = None):
        rpc_calls = {}
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)
        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 3000, 10000]:
                    query_id = f'getPool_{self.factory_addr}_{[token0, token1, fee]}_latest'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        self.factory_addr, self.factory_abi, fn_name="getPool", fn_paras=[token0, token1, fee]
                    )
        return rpc_calls

    def decode_all_supported_lp_token(self, limit: int = 100, decoded_data: dict = None, supplied_data: dict = None):
        result = {}
        top_token = supplied_data['token_info']
        length = min(len(top_token), limit)
        for idx0 in range(1, length):
            token0 = top_token[idx0]
            for idx1 in range(idx0 + 1, length):
                token1 = top_token[idx1]
                for fee in [100, 500, 3000, 10000]:
                    query_id = f'getPool_{self.factory_addr}_{[token0, token1, fee]}_latest'.lower()
                    pool_address = decoded_data.get(query_id)
                    if pool_address != '0x0000000000000000000000000000000000000000':
                        result[pool_address] = {
                            'token0': token0,
                            'token1': token1,
                            'fee': fee
                        }

        return result
