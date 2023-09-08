import logging

from web3 import Web3

from defi_services.abis.lending.aave_v3.aave_v3_incentives_abi import AAVE_V3_INCENTIVES_ABI
from defi_services.abis.lending.aave_v3.aave_v3_lending_pool_abi import AAVE_V3_LENDING_POOL_ABI
from defi_services.abis.lending.aave_v3.aave_v3_oracle_abi import AAVE_V3_ORACLE_ABI
from defi_services.abis.lending.morpho.morpho_aave_v3_comptroller_abi import MORPHO_AAVE_V3_COMPTROLLER_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.aave_v2_services import AaveV2StateService
from defi_services.services.lending.lending_info.arbitrum.aave_v3_arbitrum import AAVE_V3_ARB
from defi_services.services.lending.lending_info.avalanche.aave_v3_avalanche import AAVE_V3_AVALANCHE
from defi_services.services.lending.lending_info.ethereum.aave_v3_eth import AAVE_V3_ETH
from defi_services.services.lending.lending_info.fantom.aave_v3_ftm import AAVE_V3_FTM
from defi_services.services.lending.lending_info.optimism.aave_v3_optimism import AAVE_V3_OPTIMISM
from defi_services.services.lending.lending_info.polygon.aave_v3_polygon import AAVE_V3_POLYGON

logger = logging.getLogger("Aave V3 Lending Pool State Service")


class AaveV3Info:
    mapping = {
        Chain.ethereum: AAVE_V3_ETH,
        Chain.polygon: AAVE_V3_POLYGON,
        Chain.avalanche: AAVE_V3_AVALANCHE,
        Chain.fantom: AAVE_V3_FTM,
        Chain.optimism: AAVE_V3_OPTIMISM,
        Chain.arbitrum: AAVE_V3_ARB
    }


class AaveV3StateService(AaveV2StateService):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__(state_service, chain_id)
        self.name = f"{chain_id}_{Lending.aave_v3}"
        self.chain_id = chain_id
        self.pool_info = AaveV3Info.mapping.get(chain_id)
        self.lending_abi = AAVE_V3_LENDING_POOL_ABI
        self.incentive_abi = AAVE_V3_INCENTIVES_ABI
        self.oracle_abi = AAVE_V3_ORACLE_ABI
        self.comptroller_abi = MORPHO_AAVE_V3_COMPTROLLER_ABI
        self.state_service = state_service

    def get_service_info(self):
        info = {
            Lending.aave_v3: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(self, block_number: int = 'latest'):
        _w3 = self.state_service.get_w3()
        incentive_address = self.pool_info.get("stakedIncentiveAddress")
        pool_address = self.pool_info.get("address")
        incentive_contract = _w3.eth.contract(address=_w3.toChecksumAddress(incentive_address), abi=self.incentive_abi)
        pool_contract = _w3.eth.contract(address=_w3.toChecksumAddress(pool_address), abi=self.lending_abi)
        reward_tokens = [i.lower() for i in incentive_contract.functions.getRewardsList().call(block_identifier=block_number)]
        reserve_list = pool_contract.functions.getReservesList().call(block_identifier=block_number)
        reserves_info = {}
        for token in reserve_list:
            token = token.lower()
            reserve_data = pool_contract.functions.getReserveData(
                _w3.toChecksumAddress(token)).call(block_identifier=block_number)
            reserves_info[token] = {}
            reserves_info[token]["tToken"] = reserve_data[8].lower()
            reserves_info[token]["sdToken"] = reserve_data[9].lower()
            reserves_info[token]["dToken"] = reserve_data[10].lower()
            risk_param = bin(reserve_data[0][0])[2:]
            reserves_info[token]["liquidationThreshold"] = int(risk_param[-31:-16], 2) / 10 ** 4

        return reward_tokens, reserves_info

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest",
            is_oracle_price: bool = False  # get price by oracle
    ):
        rpc_calls = {}
        if is_oracle_price:
            asset_price_key = f"getAssetsPrices_{self.name}_{block_number}".lower()
            rpc_calls[asset_price_key] = self.get_function_oracle_info(
                "getAssetsPrices", list(reserves_info.keys()), block_number)
        reward_tokens = self.pool_info.get("rewardTokensList")
        for token_address, value in reserves_info.items():
            reserve_key = f"getReserveData_{self.name}_{token_address}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{value["tToken"]}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{value["dToken"]}_{block_number}'.lower()
            sdebt_token_total_supply_key = f'totalSupply_{value["sdToken"]}_{block_number}'.lower()
            decimals_key = f"decimals_{token_address}_{block_number}".lower()
            for reward_token in reward_tokens:
                atoken_assets_key = f"getRewardsData_{value['tToken']}_{reward_token}_{block_number}".lower()
                debt_token_assets_key = f"getRewardsData_{value['dToken']}_{reward_token}_{block_number}".lower()
                sdebt_token_assets_key = f"getRewardsData_{value['sdToken']}_{reward_token}_{block_number}".lower()
                rpc_calls[atoken_assets_key] = self.get_function_incentive_info(
                    "getRewardsData", [value['tToken'], reward_token], block_number)
                rpc_calls[debt_token_assets_key] = self.get_function_incentive_info(
                    "getRewardsData", [value['dToken'], reward_token], block_number)
                rpc_calls[sdebt_token_assets_key] = self.get_function_incentive_info(
                    "getRewardsData", [value['sdToken'], reward_token], block_number)

            rpc_calls[reserve_key] = self.get_function_lending_pool_info("getReserveData", [token_address])
            rpc_calls[atoken_total_supply_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[debt_token_total_supply_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[sdebt_token_total_supply_key] = self.state_service.get_function_info(
                value["sdToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token_address, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def get_apy_lending_pool(
            self,
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
            pool_decimals: int = 18,
            is_oracle_price: bool = False  # get price by oracle
    ):
        if not is_oracle_price:
            wrapped_native_token_price = 1
        reward_tokens = self.pool_info.get("rewardTokensList")
        for token_address in reserves_info:
            atoken = atokens.get(token_address)
            debt_token = debt_tokens.get(token_address)
            decimal = decimals.get(token_address)
            total_supply_t = total_supply_tokens.get(atoken, 0)
            total_supply_d = total_supply_tokens.get(debt_token, 0)
            # update deposit, borrow apy
            total_supply_t = total_supply_t / 10 ** decimal
            total_supply_d = total_supply_d / 10 ** decimal
            token_price = token_prices.get(token_address)
            interest_rate[token_address].update({
                "utilization": total_supply_d / total_supply_t,
            })
            total_supply_t_in_usd = total_supply_t * token_price * wrapped_native_token_price
            total_supply_d_in_usd = total_supply_d * token_price * wrapped_native_token_price
            if reward_tokens:
                interest_rate[token_address][DBConst.reward_deposit_apy] = {}
                interest_rate[token_address][DBConst.reward_borrow_apy] = {}
                asset_data_t = asset_data_tokens.get(atoken)
                asset_data_d = asset_data_tokens.get(debt_token)
                # update deposit, borrow apy
                for reward_address in reward_tokens:
                    eps_t = asset_data_t[reward_address][1] / 10 ** 18
                    eps_d = asset_data_d[reward_address][1] / 10 ** 18
                    if total_supply_t:
                        deposit_apr = eps_t * TimeConstants.A_YEAR * pool_token_price / (
                                total_supply_t * token_price)
                    else:
                        deposit_apr = 0
                    if total_supply_d:
                        borrow_apr = eps_d * TimeConstants.A_YEAR * pool_token_price / (
                                total_supply_d * token_price)
                    else:
                        borrow_apr = 0
                    interest_rate[token_address][DBConst.reward_deposit_apy].update({
                        DBConst.reward_borrow_apy: deposit_apr}
                    )
                    interest_rate[token_address][DBConst.reward_borrow_apy].update({
                        reward_address: borrow_apr}
                    )
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
            get_reserve_data_call_id = f'getReserveData_{self.name}_{token}_{block_number}'.lower()
            reserves_data[token.lower()] = decoded_data.get(get_reserve_data_call_id)
        reward_tokens = self.pool_info.get("rewardTokensList")
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

            atoken_total_supply_key = f'totalSupply_{atoken}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{debt_token}_{block_number}'.lower()
            sdebt_token_total_supply_key = f'totalSupply_{sdebt_token}_{block_number}'.lower()
            asset_data_tokens[atoken] = {}
            asset_data_tokens[debt_token] = {}
            asset_data_tokens[sdebt_token] = {}
            total_supply_tokens[atoken] = {}
            for reward_token in reward_tokens:
                atoken_assets_key = f"getRewardsData_{atoken}_{reward_token}_{block_number}".lower()
                debt_token_assets_key = f"getRewardsData_{debt_token}_{reward_token}_{block_number}".lower()
                sdebt_token_assets_key = f"getRewardsData_{sdebt_tokens}_{reward_token}_{block_number}".lower()
                asset_data_tokens[atoken][reward_token] = decoded_data.get(atoken_assets_key)
                asset_data_tokens[debt_token][reward_token] = decoded_data.get(debt_token_assets_key)
                asset_data_tokens[sdebt_token][reward_token] = decoded_data.get(sdebt_token_assets_key)
                total_supply_tokens[atoken][reward_token] = decoded_data.get(atoken_total_supply_key)

            atokens[lower_address] = atoken
            debt_tokens[lower_address] = debt_token
            sdebt_tokens[lower_address] = sdebt_token
            decimals[lower_address] = decoded_data.get(decimals_call_id)
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

    # REWARDS BALANCE
    def get_all_rewards_balance_function_info(
            self,
            wallet_address,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        reward_tokens = self.pool_info.get("rewardTokensList")
        for reward_token in reward_tokens:
            decimals_call_id = f"decimals_{reward_token}_{block_number}".lower()
            rpc_calls[decimals_call_id] = self.state_service.get_function_info(
                reward_token, ERC20_ABI, "decimals", block_number=block_number)
        tokens = []
        for key, value in reserves_info.items():
            tokens += [Web3.toChecksumAddress(value["tToken"]), Web3.toChecksumAddress(value["dToken"])]
        key = f"getAllUserRewards_{self.name}_{wallet_address}_{block_number}".lower()
        rpc_calls[key] = self.get_function_incentive_info("getAllUserRewards", [tokens, Web3.toChecksumAddress(wallet_address)], block_number)
        return rpc_calls

    def calculate_all_rewards_balance(
            self, decoded_data: dict, wallet_address: str, block_number: int = "latest"):
        key = f"getAllUserRewards_{self.name}_{wallet_address}_{block_number}".lower()
        rewards = decoded_data.get(key)
        result = dict(zip(*rewards))
        for key, value in result.items():
            decimals_call_id = f"decimals_{key}_{block_number}".lower()
            value /= 10**decoded_data.get(decimals_call_id)
            result[key] = {"amount": value}
        return result
