from web3 import Web3

from abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from abis.lending.aave_v2_and_forlks.staked_incentives_abi import STAKED_INCENTIVES_ABI
from abis.token.erc20_abi import ERC20_ABI
from constants.chain_constant import Chain
from constants.db_constant import DBConst
from constants.time_constant import TimeConstants
from jobs.state_querier import StateQuerier
from services.lending.lending_info.ethereum.aave_v2_eth import AAVE_V2_ETH
from services.lending.lending_info.polygon.aave_v2_polygon import AAVE_V2_POLYGON


class AaveInfo:
    mapping = {
        Chain.ethereum: AAVE_V2_ETH,
        Chain.polygon: AAVE_V2_POLYGON,
    }


class AaveV2StateService:
    def __init__(self, provider_uri: str, chain_id: str = "0x1"):
        self.name = f"{chain_id}_aave_v2"
        self.aave_info = AaveInfo.mapping.get(chain_id)
        self.lending_abi = LENDING_POOL_ABI
        self.incentive_abi = STAKED_INCENTIVES_ABI
        self.oracle_abi = ORACLE_ABI
        self.state_service = StateQuerier(provider_uri)

    def get_function_info(
            self,
            wallet_info: bool = False,
            apy_info: bool = False,
            wallet_reward: bool = False,
            wallet: str = None,
            reserve_info: dict = None,
            block_number: int = "latest",
            get_price: bool = "false"
    ):
        if not reserve_info:
            reserve_info = self.aave_info['reservesList']
        rpc_calls = {}
        if wallet_info and wallet:
            rpc_calls.update(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserve_info, block_number, get_price
            ))

        if apy_info:
            rpc_calls.update(self.get_apy_lending_pool_function_info(reserve_info, block_number, get_price))

        if wallet_reward:
            rpc_calls.update(self.get_rewards_balance_function_info(wallet, reserve_info, block_number))

        return rpc_calls

    def get_function_lending_pool_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.aave_info['address'], self.lending_abi, fn_name, fn_paras, block_number
        )

    def get_function_incentive_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.aave_info['stakedIncentiveAddress'], self.incentive_abi, fn_name, fn_paras, block_number
        )

    def get_function_oracle_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.aave_info['oracleAddress'], self.oracle_abi, fn_name, fn_paras, block_number
        )

    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
            get_price: bool = False,
    ):
        rpc_calls = {}
        if get_price:
            asset_price_key = f"getAssetsPrices_{self.name}_{block_number}".lower()
            rpc_calls[asset_price_key] = self.get_function_oracle_info(
                "getAssetsPrices", list(reserves_info.keys()), block_number)

        for token_address, value in reserves_info.items():
            reserve_key = f"getReserveData_{token_address}_{block_number}".lower()
            atoken_assets_key = f"assets_{value['tToken']}_{block_number}".lower()
            debt_token_assets_key = f"assets_{value['dToken']}_{block_number}".lower()
            sdebt_token_assets_key = f"assets_{value['sdToken']}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{value["tToken"]}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{value["dToken"]}_{block_number}'.lower()
            sdebt_token_total_supply_key = f'totalSupply_{value["sdToken"]}_{block_number}'.lower()
            decimals_key = f"decimals_{token_address}_{block_number}".lower()

            rpc_calls[reserve_key] = self.get_function_lending_pool_info("getReserveData", [token_address])
            rpc_calls[atoken_assets_key] = self.get_function_incentive_info("assets", [value['tToken']], block_number)
            rpc_calls[debt_token_assets_key] = self.get_function_incentive_info(
                "assets", [value['dToken']], block_number)
            rpc_calls[sdebt_token_assets_key] = self.get_function_incentive_info(
                "assets", [value['sdToken']], block_number)
            rpc_calls[atoken_total_supply_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[debt_token_total_supply_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[sdebt_token_total_supply_key] = self.state_service.get_function_info(
                value["sdToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token_address, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            get_price: bool = False,
    ):
        rpc_calls = {}
        if get_price:
            asset_price_key = f"getAssetsPrices_{self.name}_{block_number}".lower()
            rpc_calls[asset_price_key] = self.get_function_oracle_info(
                "getAssetsPrices", list(reserves_info.keys()), block_number)

        for token in reserves_info:
            value = reserves_info[token]
            atoken_balance_of_key = f'balanceOf_{value["tToken"]}_{wallet}_{block_number}'.lower()
            debt_token_balance_of_key = f'balanceOf_{value["dToken"]}_{wallet}_{block_number}'.lower()
            sdebt_token_balance_of_key = f'balanceOf_{value["sdToken"]}_{wallet}_{block_number}'.lower()
            decimals_key = f"decimals_{token}_{block_number}".lower()

            rpc_calls[atoken_balance_of_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)
            rpc_calls[debt_token_balance_of_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)
            rpc_calls[sdebt_token_balance_of_key] = self.state_service.get_function_info(
                value["sdToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)

            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def get_rewards_balance_function_info(
            self,
            wallet_address,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        tokens = [Web3.toChecksumAddress(token) for token in list(reserves_info.keys())]
        rpc_calls[f"getRewardsBalance_{wallet_address}_{block_number}".lower()] = \
            self.get_function_incentive_info("getRewardsBalance", [tokens, wallet_address], block_number)
        return rpc_calls

    @staticmethod
    def get_apy_lending_pool(
            atokens: dict,
            debt_tokens: dict,
            decimals: dict,
            reserves_info: dict,
            asset_data_tokens: dict,
            total_supply_tokens: dict,
            interest_rate: dict,
            token_prices: dict,
            pool_token_price: float,
            wrapped_native_token_price: float = 1900,
            pool_decimals: int = 18
    ):
        for token_address in reserves_info:
            atoken = atokens.get(token_address)
            debt_token = debt_tokens.get(token_address)
            decimal = decimals.get(token_address)
            total_supply_t = total_supply_tokens.get(atoken)
            total_supply_d = total_supply_tokens.get(debt_token)
            asset_data_t = asset_data_tokens.get(atoken)
            asset_data_d = asset_data_tokens.get(debt_token)
            # update deposit, borrow apy
            total_supply_t = total_supply_t / 10 ** decimal
            total_supply_d = total_supply_d / 10 ** decimal
            eps_t = asset_data_t[0] / 10 ** pool_decimals
            eps_d = asset_data_d[0] / 10 ** pool_decimals
            token_price = token_prices.get(token_address)
            if total_supply_t:
                total_supply_t_in_usd = total_supply_t * token_price * wrapped_native_token_price
                deposit_apr = eps_t * TimeConstants.A_YEAR * pool_token_price / (
                    total_supply_t_in_usd)
            else:
                total_supply_t_in_usd = 0
                deposit_apr = 0
            if total_supply_d:
                total_supply_d_in_usd = total_supply_d * token_price * wrapped_native_token_price
                borrow_apr = eps_d * TimeConstants.A_YEAR * pool_token_price / (
                    total_supply_d_in_usd)
            else:
                total_supply_d_in_usd = 0
                borrow_apr = 0
            interest_rate[token_address].update({
                "utilization": total_supply_d / total_supply_t,
                DBConst.reward_deposit_apy: deposit_apr,
                DBConst.reward_borrow_apy: borrow_apr})
            # update liquidity
            liquidity_log = {
                DBConst.total_borrow: {
                    DBConst.amount: total_supply_d,
                    DBConst.value_in_usd: total_supply_d_in_usd},
                DBConst.total_deposit: {
                    DBConst.amount: total_supply_t,
                    DBConst.value_in_usd: total_supply_t_in_usd}
            }
            interest_rate[token_address].update({DBConst.liquidity_change_logs: liquidity_log})

        return interest_rate

    @staticmethod
    def get_wallet_deposit_borrow_balance(
            reserves_info,
            token_prices,
            decimals,
            deposit_amount,
            borrow_amount,
            stable_borrow_amount,
            wrapped_native_token_price: float = 1900
    ):
        total_borrow, result = 0, {
            "borrow_amount_in_usd": 0,
            "deposit_amount_in_usd": 0,
            "health_factor": 0,
            "reserves_data": {}
        }
        for token in reserves_info:
            value = reserves_info[token]
            decimals_token = decimals.get(token)
            deposit_amount_wallet = deposit_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet = borrow_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet += stable_borrow_amount.get(token) / 10 ** decimals_token
            deposit_amount_wallet *= wrapped_native_token_price
            borrow_amount_wallet *= wrapped_native_token_price
            deposit_amount_in_usd = deposit_amount_wallet * token_prices.get(token, 0)
            borrow_amount_in_usd = borrow_amount_wallet * token_prices.get(token, 0)
            total_borrow += borrow_amount_in_usd
            result['health_factor'] += deposit_amount_in_usd * value["liquidationThreshold"]
            result['borrow_amount_in_usd'] += borrow_amount_in_usd
            result['deposit_amount_in_usd'] += deposit_amount_in_usd
            if (borrow_amount_wallet > 0) or (deposit_amount_wallet > 0):
                result['reserves_data'][token] = {
                    "borrow_amount": borrow_amount_wallet,
                    "borrow_amount_in_usd": borrow_amount_in_usd,
                    "deposit_amount": deposit_amount_wallet,
                    "deposit_amount_in_usd": deposit_amount_in_usd,
                }

        if total_borrow != 0:
            result['health_factor'] /= total_borrow
        else:
            result['health_factor'] = 100
        return result

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            wrapped_native_token_price: float = 1900,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ):
        reserves_data = {}
        for token in reserves_info:
            get_reserve_data_call_id = f'getReserveData_{token}_{block_number}'.lower()
            reserves_data[token.lower()] = decoded_data.get(get_reserve_data_call_id)

        interest_rate, atokens, debt_tokens, sdebt_tokens, decimals, asset_data_tokens = {}, {}, {}, {}, {}, {}
        total_supply_tokens = {}
        for token_address in reserves_info:
            lower_address = token_address.lower()
            reserve_data = reserves_data[lower_address]
            interest_rate[lower_address] = {
                DBConst.deposit_apy: float(reserve_data[3]) / 10 ** 27,
                DBConst.borrow_apy: float(reserve_data[4]) / 10 ** 27,
                DBConst.stable_borrow_apy: float(reserve_data[5]) / 10 ** 27}
            atoken = reserve_data[7].lower()
            sdebt_token = reserve_data[8].lower()
            debt_token = reserve_data[9].lower()
            decimals_call_id = f"decimals_{token_address}_{block_number}".lower()
            atoken_assets_key = f"assets_{atoken}_{block_number}".lower()
            debt_token_assets_key = f"assets_{debt_token}_{block_number}".lower()
            sdebt_token_assets_key = f"assets_{sdebt_token}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{atoken}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{debt_token}_{block_number}'.lower()
            sdebt_token_total_supply_key = f'totalSupply_{sdebt_token}_{block_number}'.lower()

            atokens[lower_address] = atoken
            debt_tokens[lower_address] = debt_token
            sdebt_tokens[lower_address] = sdebt_token
            decimals[lower_address] = decoded_data.get(decimals_call_id)
            asset_data_tokens[atoken] = decoded_data.get(atoken_assets_key)
            asset_data_tokens[debt_token] = decoded_data.get(debt_token_assets_key)
            asset_data_tokens[sdebt_token] = decoded_data.get(sdebt_token_assets_key)
            total_supply_tokens[atoken] = decoded_data.get(atoken_total_supply_key)
            total_supply_tokens[debt_token] = decoded_data.get(debt_token_total_supply_key)
            total_supply_tokens[sdebt_token] = decoded_data.get(sdebt_token_total_supply_key)

        asset_price_key = f"getAssetsPrices_{self.name}_{block_number}".lower()
        if not token_prices and asset_price_key in decoded_data:
            token_prices = {}
            prices = decoded_data.get(asset_price_key)
            for pos in range(len(reserves_info.keys())):
                token_prices[reserves_info[pos].lower()] = prices[pos] / 10 ** pool_decimals

        data = self.get_apy_lending_pool(
            atokens, debt_tokens, decimals, reserves_info, asset_data_tokens, total_supply_tokens, interest_rate,
            token_prices, pool_token_price, wrapped_native_token_price, pool_decimals
        )

        return data

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            wrapped_native_token_price: float = 1900,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ):
        asset_price_key = f"getAssetsPrices_{self.name}_{block_number}".lower()
        if not token_prices and asset_price_key in decoded_data:
            token_prices = {}
            prices = decoded_data.get(asset_price_key)
            for pos in range(len(reserves_info.keys())):
                token_prices[reserves_info[pos].lower()] = prices[pos] / 10 ** pool_decimals

        decimals, deposit_amount, borrow_amount, stable_borrow_amount = {}, {}, {}, {}
        for token in reserves_info:
            value = reserves_info[token]
            get_total_deposit_id = f"balanceOf_{value['tToken']}_{wallet}_{block_number}".lower()
            get_total_borrow_id = f"balanceOf_{value['dToken']}_{wallet}_{block_number}".lower()
            get_total_stable_borrow_id = f"balanceOf_{value['sdToken']}_{wallet}_{block_number}".lower()
            get_decimals_id = f"decimals_{token}_{block_number}".lower()
            deposit_amount[token] = decoded_data.get(get_total_deposit_id)
            borrow_amount[token] = decoded_data.get(get_total_borrow_id)
            stable_borrow_amount[token] = decoded_data.get(get_total_stable_borrow_id)
            decimals[token] = decoded_data.get(get_decimals_id)

        data = self.get_wallet_deposit_borrow_balance(
            reserves_info, token_prices, decimals, deposit_amount,
            borrow_amount, stable_borrow_amount, wrapped_native_token_price
        )

        return data

    @staticmethod
    def calculate_rewards_balance(self, decoded_data: dict, wallet_address: str, block_number: int = "latest"):
        reward = decoded_data.get(f"getRewardsBalance_{wallet_address}_{block_number}".lower())

        return reward / 10 ** 18
