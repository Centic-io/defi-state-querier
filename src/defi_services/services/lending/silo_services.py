import logging
import time

from defi_services.abis.lending.cream.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.lending.silo.silo_abi import SILO_ABI
from defi_services.abis.lending.silo.silo_lens_abi import SILO_LENS_ABI
from defi_services.abis.lending.silo.silo_repository_abi import SILO_REPOSITORY_ABI
from defi_services.abis.lending.silo.silo_reward_abi import SILO_REWARD_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.arbitrum.silo_arbitrum import SILO_ARBITRUM
from defi_services.services.lending.lending_info.ethereum.silo_eth import SILO_ETH
from defi_services.services.lending.lending_info.ethereum.silo_llama_eth import SILO_LLAMA_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Compound Lending Pool State Service")


class SiloInfo:
    mapping = {
        Chain.ethereum: SILO_ETH,
        Chain.arbitrum: SILO_ARBITRUM
    }


class SiloLlamaInfo:
    mapping = {
        Chain.ethereum: SILO_LLAMA_ETH
    }


class SiloStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1", llama_version: bool = True):
        self.name = f"{chain_id}_{Lending.silo}"
        self.chain_id = chain_id
        if Chain.ethereum == chain_id and llama_version:
            self.pool_info = SiloLlamaInfo.mapping.get(chain_id)
        else:
            self.pool_info = SiloInfo.mapping.get(chain_id)
        self.state_service = state_service
        self.lens_abi = SILO_LENS_ABI
        self.repository_abi = SILO_REPOSITORY_ABI
        self.reward_abi = SILO_REWARD_ABI
        self.silo_abi = SILO_ABI

    # BASIC FUNCTIONS
    def get_service_info(self):
        info = {
            Lending.silo: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(
            self,
            block_number: int = "latest",
            tokens: list = None
    ):
        _w3 = self.state_service.get_w3()
        repository_contract = _w3.eth.contract(
            address=_w3.toChecksumAddress(self.pool_info.get("repositoryAddress")), abi=self.repository_abi)
        result = {}
        for token in tokens:
            silo_token = repository_contract.functions.getSilo().call(block_identifier=block_number)
            if not silo_token: continue
            contract = _w3.eth.contract(address=_w3.toChecksumAddress(silo_token), abi=self.silo_abi)
            assets = contract.functions.getAssets().call()
            main_asset = contract.functions.siloAsset().call()
            all_assets = [i.lower() for i in assets]
            result[main_asset.lower()] = {
                'pool': token.lower(),
                'assets': all_assets
            }

        return result

    def get_token_list(self):
        begin = time.time()
        tokens = [self.pool_info.get('rewardToken'), self.pool_info.get("poolToken")]
        for token in self.pool_info.get("reservesList"):
            if token == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
                continue
            tokens.append(token)

        logger.info(f"Get token list related in {time.time() - begin}s")
        return tokens

    def get_data(
            self,
            query_types: list,
            wallet: str,
            decoded_data: dict,
            block_number: int = 'latest',
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", self.pool_info.get("reservesList"))
        token_prices = kwargs.get("token_prices", {})
        result = {}
        if Query.deposit_borrow in query_types and wallet:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            result.update(self.calculate_claimable_rewards_balance(
                wallet, decoded_data, block_number
            ))

        logger.info(f"Process protocol data in {time.time() - begin}")
        return result

    def get_function_info(
            self,
            query_types: list,
            wallet: str = None,
            block_number: int = "latest",
            **kwargs
    ):
        begin = time.time()
        reserves_info = kwargs.get("reserves_info", {})
        if not reserves_info:
            reserves_info = self.pool_info['reservesList']
        rpc_calls = {}
        if Query.deposit_borrow in query_types and wallet:
            rpc_calls.update(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            rpc_calls.update(self.get_claimable_rewards_balance_function_info(wallet, block_number))

        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return rpc_calls

    # REWARDS BALANCE
    def get_claimable_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        reward_address = self.pool_info.get('rewardAddress')
        reward_token = self.pool_info.get('rewardToken')
        rpc_call = self.state_service.get_function_info(
            reward_address, self.reward_abi, "getUserUnclaimedRewards", [wallet_address], block_number)
        decimals_call = self.state_service.get_function_info(
            reward_token, ERC20_ABI, "decimals", [], block_number)
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet_address}_{block_number}".lower()
        decimals_id = f"decimals_{self.name}_{reward_token}_{block_number}".lower()
        return {get_reward_id: rpc_call, decimals_id: decimals_call}

    def calculate_claimable_rewards_balance(self, wallet_address: str, decoded_data: dict,
                                            block_number: int = "latest"):
        reward_token = self.pool_info.get("rewardToken")
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet_address}_{block_number}".lower()
        decimals_id = f"decimals_{self.name}_{reward_token}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id) / 10 ** decoded_data.get(decimals_id)
        result = {
            reward_token: {"amount": rewards}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet_address: str,
            reserves_info: dict,
            block_number: int = "latest"
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            silo_pool = value.get('pool')
            assets = value.get('assets')
            for asset in assets:
                deposit_key = f"collateralBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet_address}_{block_number}".lower()
                borrow_key = f"debtBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet_address}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                rpc_calls[decimals_key] = self.state_service.get_function_info(
                    asset, ERC20_ABI, "decimals", [], block_number)
                rpc_calls[deposit_key] = self.get_lens_function_info(
                    "collateralBalanceOfUnderlying", [silo_pool, asset, wallet_address], block_number)
                rpc_calls[borrow_key] = self.get_lens_function_info(
                    "debtBalanceOfUnderlying", [silo_pool, asset, wallet_address], block_number
                )

        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self, wallet_address: str, reserves_info: dict, decoded_data: dict, token_prices: dict = None,
            block_number: int = "latest"):
        if token_prices is None:
            token_prices = {}
        result = {}
        for token, value in reserves_info.items():
            underlying = token
            silo_pool = value.get('pool')
            assets = value.get('assets')
            for asset in assets:
                deposit_key = f"collateralBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet_address}_{block_number}".lower()
                borrow_key = f"debtBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet_address}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                decimals = decoded_data.get(decimals_key)
                deposit_amount = decoded_data.get(deposit_key) / 10 ** decimals
                borrow_amount = decoded_data.get(borrow_key) / 10 ** decimals
                if asset not in result:
                    result[asset] = {
                        "borrow_amount": borrow_amount,
                        "deposit_amount": deposit_amount,
                    }
                else:
                    result[asset]["borrow_amount"] += borrow_amount
                    result[asset]["deposit_amount"] += deposit_amount

                if token_prices:
                    token_price = token_prices.get(underlying)
                else:
                    token_price = None
                if token_price is not None:
                    deposit_amount_in_usd = deposit_amount * token_price
                    borrow_amount_in_usd = borrow_amount * token_price
                    if 'borrow_amount_in_usd' in result[asset]:
                        result[asset]['borrow_amount_in_usd'] += borrow_amount_in_usd
                        result[asset]['deposit_amount_in_usd'] += deposit_amount_in_usd
                    else:
                        result[asset]['borrow_amount_in_usd'] = borrow_amount_in_usd
                        result[asset]['deposit_amount_in_usd'] = deposit_amount_in_usd

        return result

    def get_lens_function_info(self, fn_name: str, fn_paras: list, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )
