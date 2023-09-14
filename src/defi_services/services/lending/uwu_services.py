import logging
import time

from web3 import Web3

from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.aave_v2_and_forlks.uwu_incentives_abi import UWU_INCENTIVES_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.time_constant import TimeConstants
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.ethereum.uwu_eth import UWU_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("UWU Lending Pool State Service")


class UwuInfo:
    mapping = {
        Chain.ethereum: UWU_ETH,
    }


class UwuStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__()
        self.name = f"{chain_id}_{Lending.uwu}"
        self.chain_id = chain_id
        self.pool_info = UwuInfo.mapping.get(chain_id)
        self.lending_abi = LENDING_POOL_ABI
        self.incentive_abi = UWU_INCENTIVES_ABI
        self.oracle_abi = ORACLE_ABI
        self.state_service = state_service

    # BASIC FUNCTION
    def get_service_info(self):
        info = {
            Lending.uwu: {
                "chain_id": self.chain_id,
                "type": "lending",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_dapp_asset_info(self, block_number: int = 'latest'):
        begin = time.time()
        _w3 = self.state_service.get_w3()
        pool_address = Web3.toChecksumAddress(self.pool_info['address'])
        contract = _w3.eth.contract(address=pool_address, abi=self.lending_abi)
        reserves_list = contract.functions.getReservesList().call(block_identifier=block_number)
        reserves_info = {}
        for token in reserves_list:
            value = contract.functions.getReserveData(token).call(block_identifier=block_number)
            key = token.lower()
            reserves_info[key] = {}
            reserves_info[key]["tToken"] = value[7].lower()
            reserves_info[key]["dToken"] = value[9].lower()
            reserves_info[key]["sdToken"] = value[8].lower()
            risk_param = bin(value[0][0])[2:]
            reserves_info[key]["liquidationThreshold"] = int(risk_param[-31:-16], 2) / 10 ** 4
        logger.info(f"Get reserves information in {time.time() - begin}s")
        return reserves_info

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, value in reserves_info.items():
            reserve_key = f"getReserveData_{self.name}_{token_address}_{block_number}".lower()
            atoken_assets_key = f"assets_{value['tToken']}_{block_number}".lower()
            debt_token_assets_key = f"assets_{value['dToken']}_{block_number}".lower()
            # sdebt_token_assets_key = f"assets_{value['sdToken']}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{value["tToken"]}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{value["dToken"]}_{block_number}'.lower()
            # sdebt_token_total_supply_key = f'totalSupply_{value["sdToken"]}_{block_number}'.lower()
            decimals_key = f"decimals_{token_address}_{block_number}".lower()

            rpc_calls[reserve_key] = self.get_function_lending_pool_info("getReserveData", [token_address])
            rpc_calls[atoken_assets_key] = self.get_function_incentive_info("assets", [value['tToken']], block_number)
            rpc_calls[debt_token_assets_key] = self.get_function_incentive_info(
                "assets", [value['dToken']], block_number)
            # rpc_calls[sdebt_token_assets_key] = self.get_function_incentive_info(
            #     "assets", [value['sdToken']], block_number)
            rpc_calls[atoken_total_supply_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[debt_token_total_supply_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            # rpc_calls[sdebt_token_total_supply_key] = self.state_service.get_function_info(
            #     value["sdToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token_address, ERC20_ABI, "decimals", block_number=block_number)

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
            pool_decimals: int = 18,
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
                total_supply_t_in_usd = total_supply_t * token_price
                deposit_apr = eps_t * TimeConstants.A_YEAR * pool_token_price / (
                    total_supply_t_in_usd)
            else:
                total_supply_t_in_usd = 0
                deposit_apr = 0
            if total_supply_d:
                total_supply_d_in_usd = total_supply_d * token_price
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

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ):
        reserves_data = {}
        for token in reserves_info:
            get_reserve_data_call_id = f'getReserveData_{self.name}_{token}_{block_number}'.lower()
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
            token_prices, pool_token_price, pool_decimals
        )

        return data

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token in reserves_info:
            value = reserves_info[token]
            atoken_balance_of_key = f'balanceOf_{value["tToken"]}_{wallet}_{block_number}'.lower()
            debt_token_balance_of_key = f'balanceOf_{value["dToken"]}_{wallet}_{block_number}'.lower()
            # sdebt_token_balance_of_key = f'balanceOf_{value["sdToken"]}_{wallet}_{block_number}'.lower()
            decimals_key = f"decimals_{token}_{block_number}".lower()

            rpc_calls[atoken_balance_of_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)
            rpc_calls[debt_token_balance_of_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)
            # rpc_calls[sdebt_token_balance_of_key] = self.state_service.get_function_info(
            #     value["sdToken"], ERC20_ABI, "balanceOf", [wallet], block_number=block_number)

            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    @staticmethod
    def get_wallet_deposit_borrow_balance(
            reserves_info,
            token_prices,
            decimals,
            deposit_amount,
            borrow_amount,
    ):
        result = {}
        for token in reserves_info:
            decimals_token = decimals.get(token)
            deposit_amount_wallet = deposit_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet = borrow_amount.get(token) / 10 ** decimals_token
            # borrow_amount_wallet += stable_borrow_amount.get(token) / 10 ** decimals_token
            result[token] = {
                "borrow_amount": borrow_amount_wallet,
                "deposit_amount": deposit_amount_wallet,
            }
            if token_prices:
                deposit_amount_in_usd = deposit_amount_wallet * token_prices.get(token, 0)
                borrow_amount_in_usd = borrow_amount_wallet * token_prices.get(token, 0)
                result[token].update({
                    "borrow_amount_in_usd": borrow_amount_in_usd,
                    "deposit_amount_in_usd": deposit_amount_in_usd,
                })
        return result

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
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
            # get_total_stable_borrow_id = f"balanceOf_{value['sdToken']}_{wallet}_{block_number}".lower()
            get_decimals_id = f"decimals_{token}_{block_number}".lower()
            deposit_amount[token] = decoded_data.get(get_total_deposit_id)
            borrow_amount[token] = decoded_data.get(get_total_borrow_id)
            # stable_borrow_amount[token] = decoded_data.get(get_total_stable_borrow_id)
            decimals[token] = decoded_data.get(get_decimals_id)

        data = self.get_wallet_deposit_borrow_balance(
            reserves_info, token_prices, decimals, deposit_amount,
            borrow_amount
        )

        return data

    # REWARDS BALANCE

    def get_all_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        tokens = []
        for token, value in reserves_info.items():
            atoken, debt_token = Web3.toChecksumAddress(value['tToken']), Web3.toChecksumAddress(value['dToken'])
            tokens += [atoken, debt_token]
        key = f"claimableReward_{self.name}_{wallet}_{block_number}".lower()
        rpc_calls[key] = self.get_function_incentive_info(
            "claimableReward", [wallet, tokens], block_number)

        return rpc_calls

    def calculate_all_rewards_balance(
            self, decoded_data: dict, wallet: str, block_number: int = "latest"):
        reward_token = self.pool_info['rewardToken']
        key = f"claimableReward_{self.name}_{wallet}_{block_number}".lower()
        rewards = sum(decoded_data.get(key))/ 10 ** 18
        result = {
            reward_token: {"amount": rewards}
        }

        return result

    def get_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            atoken, debt_token = Web3.toChecksumAddress(value['tToken']), Web3.toChecksumAddress(value['dToken'])
            akey = f"claimableReward_{atoken}_{wallet}_{block_number}".lower()
            dkey = f"claimableReward_{debt_token}_{wallet}_{block_number}".lower()
            rpc_calls[akey] = self.get_function_incentive_info(
                "claimableReward", [wallet, [atoken]], block_number)
            rpc_calls[dkey] = self.get_function_incentive_info(
                "claimableReward", [wallet, [debt_token]], block_number)
        return rpc_calls

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        result = {}
        reward_token = self.pool_info['rewardToken']
        reserves_info = self.pool_info['reservesList']
        for token, value in reserves_info.items():
            atoken, debt_token = value['tToken'], value['dToken']
            akey = f"claimableReward_{atoken}_{wallet}_{block_number}".lower()
            dkey = f"claimableReward_{debt_token}_{wallet}_{block_number}".lower()
            deposit_reward = decoded_data.get(akey)[0] / 10 ** 18
            borrow_reward = decoded_data.get(dkey)[0] / 10 ** 18
            result[token] = {
                "deposit": {
                    "rewards": {
                        reward_token: {
                            "amount": deposit_reward
                        }
                    }
                },
                "borrow": {
                    "rewards": {
                        reward_token: {
                            "amount": borrow_reward
                        }
                    }
                }
            }

        return result

    def get_function_lending_pool_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['address'], self.lending_abi, fn_name, fn_paras, block_number
        )

    def get_function_incentive_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['stakedIncentiveAddress'], self.incentive_abi, fn_name, fn_paras, block_number
        )

    def get_function_oracle_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['oracleAddress'], self.oracle_abi, fn_name, fn_paras, block_number
        )
