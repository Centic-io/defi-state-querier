import logging
import time

from defi_services.abis.lending.silo.silo_abi import SILO_ABI
from defi_services.abis.lending.silo.silo_lens_abi import SILO_LENS_ABI
from defi_services.abis.lending.silo.silo_repository_abi import SILO_REPOSITORY_ABI
from defi_services.abis.lending.silo.silo_reward_abi import SILO_REWARD_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
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
        super().__init__()
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
        if not tokens:
            tokens = self.pool_info.get("reservesList").keys()
        for token in tokens:
            silo_token = repository_contract.functions.getSilo(_w3.toChecksumAddress(token)).call(block_identifier=block_number)
            if not silo_token:
                continue
            contract = _w3.eth.contract(address=_w3.toChecksumAddress(silo_token), abi=self.silo_abi)
            assets = contract.functions.getAssets().call()
            main_asset = contract.functions.siloAsset().call()
            all_assets = [i.lower() for i in assets]
            result[main_asset.lower()] = {
                'pool': silo_token.lower(),
                'assets': all_assets
            }

        return result

    def get_token_list(self):
        begin = time.time()
        reward_token = self.pool_info.get('rewardToken')
        tokens = [self.pool_info.get("poolToken")]
        if isinstance(reward_token, list):
            tokens += reward_token
        elif isinstance(reward_token, str):
            tokens.append(reward_token)

        for token, value in self.pool_info.get("reservesList").items():
            if token == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
                continue
            tokens.append(token)
            for asset in value.get("assets"):
                tokens.append(asset)
        logger.info(f"Get token list related in {time.time() - begin}s")
        tokens = list(set(tokens))
        return tokens

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, reserve_info in reserves_info.items():
            pool_address = reserve_info.get("pool")
            assets_state_query_id = f"getAssetsWithState_{pool_address}_{block_number}".lower()
            rpc_calls[assets_state_query_id] = self.get_pool_function_info(
                pool=pool_address,
                fn_name='getAssetsWithState',
                block_number=block_number
            )

            for asset_address in reserve_info['assets']:
                params = [pool_address, asset_address]

                decimals_query_id = f"decimals_{asset_address}_{block_number}".lower()
                rpc_calls[decimals_query_id] = self.state_service.get_function_info(asset_address, ERC20_ABI, "decimals", [], block_number)

                borrow_apy_query_id = f"borrowAPY_{self.pool_info['lensAddress']}_{params}_{block_number}".lower()
                rpc_calls[borrow_apy_query_id] = self.get_lens_function_info(
                    fn_name='borrowAPY',
                    fn_paras=params,
                    block_number=block_number
                )

                deposit_apy_query_id = f"depositAPY_{self.pool_info['lensAddress']}_{params}_{block_number}".lower()
                rpc_calls[deposit_apy_query_id] = self.get_lens_function_info(
                    fn_name='depositAPY',
                    fn_paras=params,
                    block_number=block_number
                )

        return rpc_calls

    def get_reserve_tokens_metadata(
            self,
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token_address, reserve_info in reserves_info.items():
            pool_address = reserve_info.get("pool")

            assets_state_query_id = f"getAssetsWithState_{pool_address}_{block_number}".lower()
            assets_state = decoded_data.get(assets_state_query_id)

            assets = []
            for asset_address, state in zip(assets_state[0], assets_state[1]):
                asset_address = asset_address.lower()

                params = [pool_address, asset_address]
                decimals_query_id = f"decimals_{asset_address}_{block_number}".lower()
                borrow_apy_query_id = f"borrowAPY_{self.pool_info['lensAddress']}_{params}_{block_number}".lower()
                deposit_apy_query_id = f"depositAPY_{self.pool_info['lensAddress']}_{params}_{block_number}".lower()

                assets.append({
                    'underlying': asset_address,
                    'underlying_decimals': decoded_data.get(decimals_query_id),
                    'supply_apy': decoded_data.get(deposit_apy_query_id),
                    'borrow_apy': decoded_data.get(borrow_apy_query_id),
                    'total_supply': state[3],
                    'total_only_deposit': state[4],
                    'total_borrow': state[5],
                    'is_base': asset_address == token_address
                })

            reserve_tokens_info.append({
                "pool": pool_address,
                "assets": assets,
            })
        return reserve_tokens_info

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = "latest",
    ):
        reserve_tokens_info = self.get_reserve_tokens_metadata(decoded_data, reserves_info, block_number)

        data = {}
        for token_info in reserve_tokens_info:
            asset_data = {}
            for asset_info in token_info['assets']:
                underlying_address = asset_info['underlying']
                asset_data[underlying_address] = self._calculate_interest_rates(asset_info, pool_decimals)
                asset_data[underlying_address]['isBase'] = asset_info.get('is_base', False)

            pool_address = token_info['pool']
            data[pool_address] = asset_data

        return data

    @classmethod
    def _calculate_interest_rates(cls, token_info: dict, pool_decimals: int):
        decimals = int(token_info["underlying_decimals"])

        total_borrow = float(token_info["total_borrow"]) / 10 ** decimals
        total_deposit = float(token_info["total_supply"]) / 10 ** decimals
        collateral_only_deposit = float(token_info["total_only_deposit"]) / 10 ** decimals
        total_supply = total_deposit + collateral_only_deposit

        supply_apy = float(token_info["supply_apy"]) / 10 ** pool_decimals
        borrow_apy = float(token_info["borrow_apy"]) / 10 ** pool_decimals

        return {
            'deposit_apy': supply_apy,
            'borrow_apy': borrow_apy,
            'total_deposit': total_supply,
            'total_borrow': total_borrow
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        reward_address = self.pool_info.get('rewardAddress')
        reward_token = self.pool_info.get('rewardToken')
        rpc_call = self.state_service.get_function_info(
            reward_address, self.reward_abi, "getUserUnclaimedRewards", [wallet], block_number)
        decimals_call = self.state_service.get_function_info(
            reward_token, ERC20_ABI, "decimals", [], block_number)
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet}_{block_number}".lower()
        decimals_id = f"decimals_{self.name}_{reward_token}_{block_number}".lower()
        return {get_reward_id: rpc_call, decimals_id: decimals_call}

    def calculate_rewards_balance(self, decoded_data: dict, wallet: str, block_number: int = "latest"):
        reward_token = self.pool_info.get("rewardToken")
        get_reward_id = f"getUserUnclaimedRewards_{self.name}_{wallet}_{block_number}".lower()
        decimals_id = f"decimals_{self.name}_{reward_token}_{block_number}".lower()
        rewards = decoded_data.get(get_reward_id) / 10 ** decoded_data.get(decimals_id)
        result = {
            reward_token: {"amount": rewards}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
            health_factor: bool = False
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            silo_pool = value.get('pool')
            assets = value.get('assets')
            if health_factor:
                key = f'getUserLiquidationThreshold_{self.name}_{silo_pool}_{wallet}_{block_number}'.lower()
                rpc_calls[key] = self.get_lens_function_info(
                    "getUserLiquidationThreshold", [silo_pool, wallet], block_number)
            for asset in assets:
                deposit_key = f"collateralBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet}_{block_number}".lower()
                borrow_key = f"debtBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                rpc_calls[decimals_key] = self.state_service.get_function_info(
                    asset, ERC20_ABI, "decimals", [], block_number)
                rpc_calls[deposit_key] = self.get_lens_function_info(
                    "collateralBalanceOfUnderlying", [silo_pool, asset, wallet], block_number)
                rpc_calls[borrow_key] = self.get_lens_function_info(
                    "debtBalanceOfUnderlying", [silo_pool, asset, wallet], block_number
                )

        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest",
            health_factor: bool = False):
        if token_prices is None:
            token_prices = {}
        result = {}
        total_borrow = 0
        total_collateral = 0
        for token, value in reserves_info.items():
            data = {}
            underlying = token
            silo_pool = value.get('pool')
            assets = value.get('assets')
            liquidation_threshold = 1
            if health_factor:
                key = f'getUserLiquidationThreshold_{self.name}_{silo_pool}_{wallet}_{block_number}'.lower()
                liquidation_threshold = decoded_data.get(key) / 10 ** 18
            for asset in assets:
                deposit_key = f"collateralBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet}_{block_number}".lower()
                borrow_key = f"debtBalanceOfUnderlying_{underlying}_{silo_pool}_{asset}_{wallet}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                decimals = decoded_data.get(decimals_key)
                deposit_amount = decoded_data.get(deposit_key) / 10 ** decimals
                borrow_amount = decoded_data.get(borrow_key) / 10 ** decimals
                if asset not in data:
                    data[asset] = {
                        "borrow_amount": borrow_amount,
                        "deposit_amount": deposit_amount,
                    }
                else:
                    data[asset]["borrow_amount"] += borrow_amount
                    data[asset]["deposit_amount"] += deposit_amount

                if token_prices:
                    token_price = token_prices.get(underlying)
                else:
                    token_price = None
                if token_price is not None:
                    deposit_amount_in_usd = deposit_amount * token_price
                    borrow_amount_in_usd = borrow_amount * token_price
                    if 'borrow_amount_in_usd' in data[asset]:
                        data[asset]['borrow_amount_in_usd'] += borrow_amount_in_usd
                        data[asset]['deposit_amount_in_usd'] += deposit_amount_in_usd
                    else:
                        data[asset]['borrow_amount_in_usd'] = borrow_amount_in_usd
                        data[asset]['deposit_amount_in_usd'] = deposit_amount_in_usd
                    total_collateral += deposit_amount_in_usd * liquidation_threshold
                    total_borrow += borrow_amount_in_usd
            result[silo_pool] = data
        if health_factor:
            if total_collateral and total_borrow:
                hf = total_collateral / total_borrow
            elif total_collateral:
                hf = 100
            else:
                hf = 0
            result["health_factor"] = hf
        return result

    # HEALTH FACTOR
    def get_health_factor_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = self.get_wallet_deposit_borrow_balance_function_info(
            wallet,
            reserves_info,
            block_number,
            True
        )
        return rpc_calls

    def calculate_health_factor(
            self,
            wallet: str,
            reserves_info,
            decoded_data: dict = None,
            token_prices: dict = None,
            pool_decimals: int = 18,
            block_number: int = "latest"
    ):
        data = self.calculate_wallet_deposit_borrow_balance(
            wallet,
            reserves_info,
            decoded_data,
            token_prices,
            pool_decimals,
            block_number,
            True
        )

        return {"health_factor": data["health_factor"]}

    def get_lens_function_info(self, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            self.pool_info['lensAddress'], self.lens_abi, fn_name, fn_paras, block_number
        )

    def get_pool_function_info(self, pool: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            pool, self.silo_abi, fn_name, fn_paras, block_number
        )
