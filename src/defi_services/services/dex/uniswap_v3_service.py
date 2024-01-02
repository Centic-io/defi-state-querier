import logging

from defi_services.abis.dex.uniswap.factory_v3_abi import UNISWAP_V3_FACTORY_ABI
from defi_services.abis.dex.uniswap.nft_token_manager_abi import UNISWAP_V3_NFT_TOKEN_MANGAGER_ABI
from defi_services.abis.dex.uniswap.pool_v3_abi import UNISWAP_V3_POOL_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.dex.dex_info.uniswap_info import UNISWAP_V3_ETH_INFO
from defi_services.services.dex_protocol_services import DexProtocolServices

logger = logging.getLogger("UniSwap V2 State Service")


class UniswapV3Info:
    mapping = {
        Chain.ethereum: UNISWAP_V3_ETH_INFO
    }


class UniswapV3Services(DexProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = '0x1'):
        super().__init__()
        self.chain_id = chain_id
        self.state_service = state_service
        self.pool_info = UniswapV3Info.mapping.get(chain_id)
        self.factory_abi = UNISWAP_V3_FACTORY_ABI
        self.nft_token_manager_addr = self.pool_info['NFT_manager_address']
        self.nft_token_manager_abi = self.pool_info['NFT_manager_abi']


    def get_service_info(self):
        info = {
            Dex.uniswap_v3: {
                "chain_id": self.chain_id,
                "type": "dex",
                "pool_info": self.pool_info
            }
        }
        return info

    def get_all_supported_lp_token(self, limit:int=100, supplied_data: dict= None):
        rpc_calls ={}
        top_token= supplied_data['token_info']
        length = min(len(top_token),limit)
        for  idx0 in range(1,length ):
            token0= top_token[idx0]
            for idx1 in range(idx0+1, length ):
                token1 = top_token[idx1]
                for fee in [100,500,3000,10000]:
                    query_id= f'allPool_{token0}_{token1}_{fee}_latest'.lower()
                    rpc_calls[query_id] = self.get_factory_function_info(fn_name="getPool", fn_paras=[token0, token1, fee])
        return rpc_calls


    def decode_all_supported_lp_token(self, decoded_data, supplied_data: dict= None) :
        result={}
        for query_id, value in decoded_data.items():
            if value!='0x0000000000000000000000000000000000000000':
                token0= query_id.split("_")[1]
                token1= query_id.split("_")[2]
                fee= query_id.split("_")[3]

                result[value]= {
                    'token0': token0,
                    'token1': token1,
                    'fee': fee
                }
        return result

    def get_lp_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            for fn_name in ["liquidity", "slot0"]:
                query_id = f"{fn_name}_{lp_token}_{block_number}_{self.chain_id}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(
                    address=lp_token, abi=UNISWAP_V3_POOL_ABI, fn_name=fn_name, fn_paras=None,
                    block_number=block_number)

        return rpc_calls

    def decode_lp_token_info(self, supplied_data, response_data, block_number: int = "latest"):
        result = {}
        lp_token_info = supplied_data['lp_token_info']
        for lp_token, value in lp_token_info.items():
            token0 = value.get("token0")
            token1 = value.get("token1")
            fee = value.get('fee')
            total_liquidity = response_data.get(f'liquidity_{lp_token}_{block_number}_{self.chain_id}'.lower(),
                                                0)
            sqrt_price_x96 = response_data.get(f"slot0_{lp_token}_{block_number}_{self.chain_id}".lower())[0]
            price = self.convert_q64_96_to_integer(sqrt_price_x96)
            result[lp_token] = {
                "token0": token0,
                'token1': token1,
                'fee': fee,
                "totalLiquidity": total_liquidity / 10 ** 18,
                "currentPrice": price,
            }
        return result

    def get_balance_of_token_function_info(self, supplied_data, block_number: int = "latest"):
        rpc_calls = {}
        lp_token_info = supplied_data['lp_token_info']
        for key, value in lp_token_info.items():
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    rpc_calls[query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="balanceOf", fn_paras=[key],
                        block_number=block_number)
                    rpc_calls[decimals_query_id] = self.state_service.get_function_info(
                        address=token, abi=ERC20_ABI, fn_name="decimals", block_number=block_number)

        return rpc_calls

    def decode_balance_of_token_function_info(
            self, supplied_data, balance_info, block_number: int = "latest"):
        lp_token_balance = {}
        lp_token_info = supplied_data['lp_token_info']
        for key, value in lp_token_info.items():
            lp_token_balance[key] = {}
            for fn_name in ["token0", "token1"]:
                token = value.get(fn_name, None)
                if token is not None:
                    query_id = f'balanceOf_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    decimals_query_id = f'decimals_{key}_{token}_{block_number}_{self.chain_id}'.lower()
                    lp_token_balance[key][token] = balance_info.get(query_id) / 10 ** balance_info.get(
                        decimals_query_id)
        result = self.calculate_lp_token_price_info(lp_token_info, lp_token_balance)
        return result

    def calculate_lp_token_price_info(
            self, lp_token_info, lp_token_balance):
        for lp_token, value in lp_token_info.items():
            token0 = value.get("token0", None)
            token1 = value.get("token1", None)
            if token0 and token1:
                balance_of_token0 = lp_token_balance[lp_token].get(token0, 0)
                balance_of_token1 = lp_token_balance[lp_token].get(token1, 0)
                lp_token_info[lp_token].update({
                    "token0Amount": balance_of_token0,
                    "token1Amount": balance_of_token1
                })
        return lp_token_info
    def get_factory_function_info(self, fn_name, fn_paras: list= None, block_number: int = 'latest'):
        factory_addr = self.pool_info['factoryAddress']
        return self.state_service.get_function_info(
            factory_addr, self.factory_abi, fn_name, fn_paras, block_number
        )

    ### USER
    def get_all_nft_token_of_user_function(
            self, user: str, block_number: int = "latest"):
        rpc_calls = {}
        web3 = self.state_service.get_w3()
        user = self.checksum_address(web3, user)
        self.nft_token_manager_addr = self.checksum_address(web3, self.nft_token_manager_addr)
        nft_contract = web3.eth.contract(abi=self.nft_token_manager_abi,
                                         address=self.nft_token_manager_addr)
        number_token = nft_contract.functions.balanceOf(user).call()
        for idx in range(number_token):
            query_id = f'tokenOfOwnerByIndex_{user}_{idx}_{block_number}_{self.chain_id}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="tokenOfOwnerByIndex",
                fn_paras=[user, idx],
                block_number=block_number)

        return rpc_calls

    def decode_all_nft_token_of_user_function(
            self, user_data: dict):
        result = {}
        for query_id, token_id in user_data.items():
            ind = query_id.split("_")[2]
            result.update(
                {token_id: {"index": ind}}
            )

        return result

    def get_user_info_function(self, user: str, supplied_data: dict, stake: bool = True, block_number: int = "latest"):
        rpc_calls = {}
        user_data= supplied_data['user_data']
        for token_id, value in user_data.items():
            query_id = f'positions_{user}_{token_id}_{block_number}'.lower()
            rpc_calls[query_id] = self.state_service.get_function_info(
                address=self.nft_token_manager_addr, abi=self.nft_token_manager_abi, fn_name="positions",
                fn_paras=[int(token_id)], block_number=block_number)

        return rpc_calls

    def decode_user_info_function(self, user: str, supplied_data: dict, decoded_data: dict= None, token_price: dict = None,
                                  stake: bool = True,
                                  block_number: int = "latest"):
        user_data= supplied_data['user_data']
        for token_id, value in user_data.items():
            query_id = f'positions_{user}_{token_id}_{block_number}'.lower()
            response = decoded_data.get(query_id)
            liquidity = response[7]
            if liquidity != 0:
                print(f'{token_id}: {liquidity}')
            user_data[token_id].update(
                {
                    "liquidity": liquidity,
                    "token0": response[2],
                    "token1": response[3],
                    'fee':  response[4],
                                    }
            )

        return user_data
    def convert_q64_96_to_integer(self, sqrt_price_x96):
        integer_part = sqrt_price_x96 >> 96
        fractional_part = (sqrt_price_x96 & ((1 << 96) - 1)) / (2 ** 96)
        # Tổng hợp thành số nguyên
        result = integer_part + fractional_part

        return result
    
    def checksum_address(self, web3, address):
        if web3.isAddress(address):
            address = web3.toChecksumAddress(address)
        return address
