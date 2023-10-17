from defi_services.abis.lending.compound_v3.comet_abi import COMET_ABI
from defi_services.abis.lending.compound_v3.comet_ext_abi import COMET_EXT_ABI
from defi_services.abis.lending.compound_v3.reward_abi import REWARD_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.compound_service import CompoundStateService
from defi_services.services.lending.lending_info.ethereum.compound_v3_eth import COMPOUND_V3_ETH


class CompoundV3Info:
    mapping = {
        Chain.ethereum: COMPOUND_V3_ETH
    }


class CompoundV3StateService(CompoundStateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.compound_v3}"
        self.pool_info = CompoundV3Info.mapping.get(chain_id)
        self.comet_abi = COMET_ABI
        self.comet_ext = COMET_EXT_ABI
        self.reward_abi = REWARD_ABI

    def get_service_info(self):
        info = {
            Lending.compound_v3: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(
            self,
            block_number: int = "latest",
            comets: list = None,
    ):
        result = {}
        w3 = self.state_service.get_w3()
        pools = [value.get('comet') for key, value in self.pool_info.get('reservesList').items()]
        if comets:
            pools += comets
        for pool in pools:
            contract = w3.eth.contract(address=w3.toChecksumAddress(pool), abi=self.comet_abi)
            base_token = contract.functions.baseToken().call().lower()
            number_assets = contract.functions.numAssets().call()
            asset_data = {}
            for i in range(number_assets):
                data = contract.functions.getAssetInfo(i).call()
                asset = data[1].lower()
                asset_data[asset] = {
                    "priceFeed": data[2].lower(),
                    "loanToValue": data[4] / 10 ** 18,
                    "liquidationThreshold": data[5] / 10 ** 18
                }
            result[base_token] = {
                "comet": pool.lower(),
                "assets": asset_data
            }
        return result

    # PROTOCOL APY
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, reserve_info in reserves_info.items():
            if token_address != Token.native_token:
                query_id = f"decimals_{token_address}_{block_number}".lower()
                rpc_calls[query_id] = self.state_service.get_function_info(token_address, ERC20_ABI, "decimals", [], block_number)

            comet_address = reserve_info['comet']
            functions = [
                'decimals', 'totalBorrow', 'getUtilization', 'borrowKink', 'borrowPerSecondInterestRateBase',
                'borrowPerSecondInterestRateSlopeHigh', 'borrowPerSecondInterestRateSlopeLow',
                'supplyKink', 'supplyPerSecondInterestRateBase', 'supplyPerSecondInterestRateSlopeHigh',
                'supplyPerSecondInterestRateSlopeLow'
            ]
            for fn_name in functions:
                query_id = f"{fn_name}_{comet_address}_{block_number}".lower()
                rpc_calls[query_id] = self.get_comet_function_info(
                    comet=comet_address,
                    fn_name=fn_name,
                    block_number=block_number
                )

            for collateral_address in reserve_info['assets']:
                decimals_query_id = f"decimals_{collateral_address}_{block_number}".lower()
                rpc_calls[decimals_query_id] = self.state_service.get_function_info(collateral_address, ERC20_ABI, "decimals", [], block_number)

                supply_query_id = f"totalsCollateral_{comet_address}_{collateral_address}_{block_number}".lower()
                rpc_calls[supply_query_id] = self.get_comet_function_info(
                    comet=comet_address,
                    fn_name='totalsCollateral',
                    fn_paras=[collateral_address],
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
            if token_address != Token.native_token:
                underlying_decimals_query_id = f"decimals_{token_address}_{block_number}".lower()
                underlying_decimals = decoded_data.get(underlying_decimals_query_id)
            else:
                underlying_decimals = Chain.native_decimals.get(self.chain_id, 18)

            comet_address = reserve_info['comet']
            comet_decimals_query_id = f"decimals_{comet_address}_{block_number}".lower()
            total_borrow_query_id = f"totalBorrow_{comet_address}_{block_number}".lower()
            utilization_query_id = f"getUtilization_{comet_address}_{block_number}".lower()

            info = {
                "token": comet_address,
                "token_decimals": decoded_data.get(comet_decimals_query_id),
                "utilization": decoded_data.get(utilization_query_id),
                'total_borrow': decoded_data.get(total_borrow_query_id),
                "underlying_decimals": underlying_decimals,
                "underlying": token_address
            }
            for lending_type in ['borrow', 'supply']:
                kink_query_id = f"{lending_type}Kink_{comet_address}_{block_number}".lower()
                base_rate_query_id = f"{lending_type}PerSecondInterestRateBase_{comet_address}_{block_number}".lower()
                jump_multiplier_query_id = f"{lending_type}PerSecondInterestRateSlopeHigh_{comet_address}_{block_number}".lower()
                multiplier_query_id = f"{lending_type}PerSecondInterestRateSlopeLow_{comet_address}_{block_number}".lower()

                info[f'{lending_type}_kink'] = decoded_data.get(kink_query_id)
                info[f'{lending_type}_base_rate'] = decoded_data.get(base_rate_query_id)
                info[f'{lending_type}_jump_multiplier'] = decoded_data.get(jump_multiplier_query_id)
                info[f'{lending_type}_multiplier'] = decoded_data.get(multiplier_query_id)

            assets = []
            for collateral_address in reserve_info['assets']:
                decimals_query_id = f"decimals_{collateral_address}_{block_number}".lower()
                supply_query_id = f"totalsCollateral_{comet_address}_{collateral_address}_{block_number}".lower()

                assets.append({
                    'underlying': collateral_address,
                    'total_supply': decoded_data.get(supply_query_id)[0],
                    'underlying_decimals': decoded_data.get(decimals_query_id)
                })
            info['assets'] = assets
            reserve_tokens_info.append(info)

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
            underlying_token = token_info['underlying']
            data[underlying_token] = self._calculate_interest_rates(
                token_info, pool_decimals=pool_decimals,
                apx_block_speed_in_seconds=0
            )

        return data

    @classmethod
    def _calculate_interest_rates(
            cls, token_info: dict, pool_decimals: int, apx_block_speed_in_seconds: float):

        total_borrow = float(token_info["total_borrow"]) / 10 ** int(token_info["underlying_decimals"])
        collaterals = {}
        for asset_info in token_info['assets']:
            collateral_address = asset_info['underlying']
            total_supply = float(asset_info["total_supply"]) / 10 ** int(asset_info["underlying_decimals"])
            collaterals[collateral_address] = total_supply

        utilization = token_info['utilization'] / 10 ** 18
        interests = {}
        for lending_type in ['borrow', 'supply']:
            kink = token_info[f'{lending_type}_kink'] / 10 ** 18
            base_rate = TimeConstants.A_YEAR * token_info[f'{lending_type}_base_rate'] / 10 ** 18
            jump_multiplier = TimeConstants.A_YEAR * token_info[f'{lending_type}_jump_multiplier'] / 10 ** 18
            multiplier = TimeConstants.A_YEAR * token_info[f'{lending_type}_multiplier'] / 10 ** 18

            interest_rate = multiplier * min(utilization, kink) + jump_multiplier * max(0, utilization - kink) + base_rate
            interests[lending_type] = interest_rate

        return {
            DBConst.deposit_apy: interests['supply'],
            DBConst.borrow_apy: interests['borrow'],
            DBConst.total_deposit: None,
            DBConst.total_borrow: total_borrow,
            DBConst.collaterals: collaterals
        }

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest",
    ):
        result = {}
        reward_address = self.pool_info.get("rewardAddress")
        for token, value in self.pool_info.get("reservesList").items():
            comet = value.get("comet")
            rpc_call = self.state_service.get_function_info(
                reward_address, self.reward_abi, "getRewardOwed", [comet, wallet], block_number)
            get_reward_id = f"getRewardOwed_{reward_address}_{comet}_{wallet}_{block_number}".lower()
            result[get_reward_id] = rpc_call
        return result

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        reward_amount = 0
        reward_address = self.pool_info.get("rewardAddress")
        for token, value in self.pool_info.get("reservesList").items():
            comet = value.get("comet")
            get_reward_id = f"getRewardOwed_{reward_address}_{comet}_{wallet}_{block_number}".lower()
            reward_amount += decoded_data.get(get_reward_id)[1] / 10 ** 18
        reward_token = self.pool_info.get("rewardToken")
        result = {
            reward_token: {"amount": reward_amount}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            health_factor: bool = False
    ):

        rpc_calls = {}
        for token, value in reserves_info.items():
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            comet = value.get('comet')
            comet_ext = value.get('comet')
            assets = value.get('assets')
            decimals_key = f"decimals_{underlying}_{block_number}".lower()
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                    underlying, ERC20_ABI, "decimals", [], block_number
                )
            borrow_key = f"borrowBalanceOf_{comet}_{underlying}_{wallet}_{block_number}".lower()
            rpc_calls[borrow_key] = self.state_service.get_function_info(
                comet, self.comet_abi, "borrowBalanceOf", [wallet], block_number)
            for asset in assets:
                balance_key = f"collateralBalanceOf_{comet_ext}_{asset}_{wallet}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                rpc_calls[balance_key] = self.state_service.get_function_info(
                    comet_ext, self.comet_ext, "collateralBalanceOf", [wallet, asset], block_number)
                rpc_calls[decimals_key] = self.state_service.get_function_info(
                    asset, ERC20_ABI, "decimals", [], block_number
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
            health_factor: bool = False
    ):
        result = {}
        total_borrow = 0
        total_collateral = 0
        for token, value in reserves_info.items():
            deposit_borrow = {}
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            comet = value.get('comet')
            comet_ext = value.get('comet')
            assets = value.get('assets')
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            borrow_key = f"borrowBalanceOf_{comet}_{underlying}_{wallet}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            borrow_amount = decoded_data[borrow_key] / 10 ** decimals
            for asset, asset_info in assets.items():
                balance_key = f"collateralBalanceOf_{comet_ext}_{asset}_{wallet}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                decimals_token = decoded_data[decimals_key]
                deposit_amount = decoded_data[balance_key] / 10 ** decimals_token
                deposit_borrow[asset] = {
                        "borrow_amount": 0,
                        "deposit_amount": deposit_amount,
                    }
                if token_prices:
                    deposit_amount_in_usd = deposit_amount * token_prices.get(asset)
                    total_collateral += deposit_amount_in_usd * asset_info.get("liquidationThreshold")

            if underlying not in deposit_borrow:
                deposit_borrow[underlying] = {
                    "borrow_amount": borrow_amount,
                    "deposit_amount": 0
                }
            else:
                deposit_borrow[underlying]["borrow_amount"] = borrow_amount

            if token_prices:
                borrow_amount_in_usd = token_prices.get(underlying)
                total_borrow += borrow_amount_in_usd

            result[comet] = deposit_borrow

        if health_factor:
            if total_collateral and total_borrow:
                result['health_factor'] = total_collateral/total_borrow
            elif total_collateral:
                result['health_factor'] = 100
            else:
                result['health_factor'] = 0

        return result

    def get_comet_function_info(self, comet: str, fn_name: str, fn_paras: list = None, block_number: int = "latest"):
        return self.state_service.get_function_info(
            comet, self.comet_abi, fn_name, fn_paras, block_number
        )
