import logging
import time

from web3 import Web3
from defi_services.abis.lending.aave_v2_and_forlks.aave_v2_incentives_abi import AAVE_V2_INCENTIVES_ABI
from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.granary.granary_rewarder_abi import GRANARY_REWARDER_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.query_constant import Query
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.bsc.granary_bsc import GRANARY_BSC
from defi_services.services.lending.lending_info.ethereum.granary_v1_eth import GRANARY_V1_ETH
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Granary V1 Lending Pool State Service")


class GranaryV1Info:
    mapping = {
        Chain.ethereum: GRANARY_V1_ETH,
        Chain.bsc: GRANARY_BSC
    }


class GranaryV1StateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        self.name = f"{chain_id}_{Lending.granary}"
        self.chain_id = chain_id
        self.pool_info = GranaryV1Info.mapping.get(chain_id)
        self.lending_abi = LENDING_POOL_ABI
        self.incentive_abi = AAVE_V2_INCENTIVES_ABI
        self.oracle_abi = ORACLE_ABI
        self.state_service = state_service
        self.rewarder_abi = GRANARY_REWARDER_ABI

    # BASIC FUNCTION
    def get_service_info(self):
        info = {
            Lending.granary: {
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
        pool_token_price = token_prices.get(self.pool_info.get('poolToken'), 1)
        wrapped_native_token_price = token_prices.get(Token.wrapped_token.get(self.chain_id), 1)
        pool_decimals = kwargs.get("pool_decimals", 18)
        result = {}
        if Query.deposit_borrow in query_types and wallet:
            result.update(self.calculate_wallet_deposit_borrow_balance(
                wallet, reserves_info, decoded_data, token_prices, wrapped_native_token_price, pool_decimals,
                block_number
            ))

        if Query.protocol_reward in query_types and wallet:
            result.update(self.calculate_all_rewards_balance(
                decoded_data, wallet, block_number
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
        is_oracle_price = kwargs.get("is_oracle_price", False)  # get price by oracle
        if not reserves_info:
            reserves_info = self.pool_info['reservesList']
        rpc_calls = {}
        if Query.deposit_borrow in query_types and wallet:
            rpc_calls.update(self.get_wallet_deposit_borrow_balance_function_info(
                wallet, reserves_info, block_number, is_oracle_price
            ))

        if Query.protocol_reward in query_types and wallet:
            rpc_calls.update(self.get_all_rewards_balance_function_info(wallet, reserves_info, block_number))
        logger.info(f"Get encoded rpc calls in {time.time() - begin}s")
        return rpc_calls

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            is_oracle_price: bool = False  # get price by oracle
    ):
        rpc_calls = {}
        if is_oracle_price:
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

    @staticmethod
    def get_wallet_deposit_borrow_balance(
            reserves_info,
            token_prices,
            decimals,
            deposit_amount,
            borrow_amount,
            stable_borrow_amount,
            wrapped_native_token_price: float = 1900,
            is_oracle_price: bool = False  # get price by oracle
    ):
        result = {}
        for token in reserves_info:
            decimals_token = decimals.get(token)
            deposit_amount_wallet = deposit_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet = borrow_amount.get(token) / 10 ** decimals_token
            borrow_amount_wallet += stable_borrow_amount.get(token) / 10 ** decimals_token
            result[token] = {
                "borrow_amount": borrow_amount_wallet,
                "deposit_amount": deposit_amount_wallet,
            }
            if token_prices:
                deposit_amount_in_usd = deposit_amount_wallet * token_prices.get(token, 0)
                borrow_amount_in_usd = borrow_amount_wallet * token_prices.get(token, 0)
                if is_oracle_price:
                    deposit_amount_wallet *= wrapped_native_token_price
                    borrow_amount_wallet *= wrapped_native_token_price
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

    # REWARDS BALANCE

    def get_all_rewards_balance_function_info(
            self,
            wallet_address,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        tokens = []
        for token, value in reserves_info.items():
            atoken, debt_token = Web3.toChecksumAddress(value['tToken']), Web3.toChecksumAddress(value['dToken'])
            tokens += [atoken, debt_token]
        key = f"getAllUserRewardsBalance_{self.name}_{wallet_address}_{block_number}".lower()
        rpc_calls[key] = self.get_function_rewarder_info(
            "getAllUserRewardsBalance", [tokens, wallet_address], block_number)

        return rpc_calls

    def calculate_all_rewards_balance(
            self, decoded_data: dict, wallet_address: str, block_number: int = "latest"):

        key = f"getAllUserRewardsBalance_{self.name}_{wallet_address}_{block_number}".lower()
        if not decoded_data.get(key)[0]:
            return {}
        reward_token = decoded_data.get(key)[0][0]
        rewards = decoded_data.get(key)[-1][0] / 10 ** 18
        result = {
            reward_token.lower(): {"amount": rewards}
        }

        return result

    def get_function_lending_pool_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['address'], self.lending_abi, fn_name, fn_paras, block_number
        )

    def get_function_rewarder_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['rewarder'], self.rewarder_abi, fn_name, fn_paras, block_number
        )

    def get_function_oracle_info(self, fn_name: str, fn_paras=None, block_number: int = 'latest'):
        return self.state_service.get_function_info(
            self.pool_info['oracleAddress'], self.oracle_abi, fn_name, fn_paras, block_number
        )
