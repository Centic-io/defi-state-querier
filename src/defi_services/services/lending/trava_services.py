import logging

from defi_services.constants.db_constant import DBConst
from defi_services.constants.time_constant import TimeConstants

logger = logging.getLogger("Trava Lending Pool State Service")


class TravaStateService:
    def __init__(self, provider_uri: str):
        super().__init__(provider_uri)

    @staticmethod
    def get_apy_lending_pool(
            atokens: dict,
            debt_tokens: dict,
            decimals: dict,
            reserves_list: list,
            asset_data_tokens: dict,
            total_supply_tokens: dict,
            interest_rate: dict,
            token_prices: dict = None,
            pool_token_price: float = 1,
    ):
        for token_address in reserves_list:
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
            eps_t = asset_data_t[1] / 10 ** 18
            eps_d = asset_data_d[1] / 10 ** 18
            token_price = token_prices.get(token_address)
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
            interest_rate[token_address].update({
                "utilization": total_supply_d / total_supply_t,
                DBConst.reward_deposit_apy: deposit_apr,
                DBConst.reward_borrow_apy: borrow_apr})
            # update liquidity
            liquidity_log = {
                DBConst.total_borrow: {
                    DBConst.amount: total_supply_d,
                    DBConst.value_in_usd: total_supply_d * token_price},
                DBConst.total_deposit: {
                    DBConst.amount: total_supply_t,
                    DBConst.value_in_usd: total_supply_t * token_price}
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
    ):
        total_borrow, result = 0, {
            "borrow_amount_in_usd": 0,
            "deposit_amount_in_usd": 0,
            "health_factor": 0,
            "reserves_data": {}
        }
        for token in reserves_info:
            value = reserves_info[token]
            decimals_token = decimals.get(value)
            deposit_amount_wallet = deposit_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet = borrow_amount.get(token) / 10 ** decimals_token

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
