import logging
import time

from web3 import Web3

from defi_services.abis.lending.aave_v2_and_forlks.aave_v2_incentives_abi import AAVE_V2_INCENTIVES_ABI
from defi_services.abis.lending.aave_v2_and_forlks.lending_pool_abi import LENDING_POOL_ABI
from defi_services.abis.lending.aave_v2_and_forlks.oracle_abi import ORACLE_ABI
from defi_services.abis.lending.granary.granary_rewarder_abi import GRANARY_REWARDER_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.db_constant import DBConst
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.lending.lending_info.arbitrum.granary_arbitrum import GRANARY_ARBITRUM
from defi_services.services.lending.lending_info.avalanche.granary_avalanche import GRANARY_AVALANCHE
from defi_services.services.lending.lending_info.bsc.granary_bsc import GRANARY_BSC
from defi_services.services.lending.lending_info.ethereum.granary_eth import GRANARY_V1_ETH
from defi_services.services.lending.lending_info.fantom.granary_ftm import GRANARY_FTM
from defi_services.services.lending.lending_info.optimism.granary_optimism import GRANARY_OPTIMISM
from defi_services.services.protocol_services import ProtocolServices

logger = logging.getLogger("Granary V1 Lending Pool State Service")


class GranaryV1Info:
    mapping = {
        Chain.ethereum: GRANARY_V1_ETH,
        Chain.bsc: GRANARY_BSC,
        Chain.optimism: GRANARY_OPTIMISM,
        Chain.fantom: GRANARY_FTM,
        Chain.avalanche: GRANARY_AVALANCHE,
        Chain.arbitrum: GRANARY_ARBITRUM
    }


class GranaryStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__()
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
        tokens = self.pool_info.get('rewardToken') + [self.pool_info.get("poolToken")]
        for token in self.pool_info.get("reservesList"):
            if token == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
                continue
            tokens.append(token)
        logger.info(f"Get token list related in {time.time() - begin}s")
        return tokens

    # CALCULATE APY LENDING POOL
    def get_apy_lending_pool_function_info(
            self,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token_address, value in reserves_info.items():
            reserve_key = f"getReserveData_{self.name}_{token_address}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{value["tToken"]}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{value["dToken"]}_{block_number}'.lower()
            decimals_key = f"decimals_{token_address}_{block_number}".lower()

            rpc_calls[reserve_key] = self.get_function_lending_pool_info("getReserveData", [token_address])
            rpc_calls[atoken_total_supply_key] = self.state_service.get_function_info(
                value["tToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[debt_token_total_supply_key] = self.state_service.get_function_info(
                value["dToken"], ERC20_ABI, "totalSupply", block_number=block_number)
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token_address, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def get_reserve_tokens_metadata(
            self,
            decoded_data: dict,
            reserves_info: dict,
            block_number: int = "latest"
    ):
        reserve_tokens_info = []
        for token_address, reserve_info in reserves_info.items():
            get_reserve_data_call_id = f'getReserveData_{self.name}_{token_address}_{block_number}'.lower()
            reserve_data = decoded_data.get(get_reserve_data_call_id)

            atoken = reserve_data[7].lower()
            debt_token = reserve_data[9].lower()
            decimals_call_id = f"decimals_{token_address}_{block_number}".lower()
            atoken_total_supply_key = f'totalSupply_{atoken}_{block_number}'.lower()
            debt_token_total_supply_key = f'totalSupply_{debt_token}_{block_number}'.lower()

            reserve_tokens_info.append({
                'underlying': token_address,
                'underlying_decimals': decoded_data.get(decimals_call_id),
                'a_token_supply': decoded_data.get(atoken_total_supply_key),
                'd_token_supply': decoded_data.get(debt_token_total_supply_key),
                'supply_apy': reserve_data[3],
                'borrow_apy': reserve_data[4]
            })

        return reserve_tokens_info

    def calculate_apy_lending_pool_function_call(
            self,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_token_price: float,
            pool_decimals: int = 18,
            block_number: int = 'latest',
    ):
        reserve_tokens_info = self.get_reserve_tokens_metadata(decoded_data, reserves_info, block_number)

        data = {}
        for token_info in reserve_tokens_info:
            underlying_token = token_info['underlying']
            data[underlying_token] = self._calculate_interest_rates(token_info)

        return data

    @classmethod
    def _calculate_interest_rates(cls, token_info: dict):
        total_supply_t = token_info.get('a_token_supply')
        total_supply_d = token_info.get('d_token_supply')

        total_supply = total_supply_t / 10 ** token_info['underlying_decimals']
        total_borrow = total_supply_d / 10 ** token_info['underlying_decimals']

        supply_apy = float(token_info['supply_apy']) / 10 ** 27
        borrow_apy = float(token_info['borrow_apy']) / 10 ** 27

        return {
            DBConst.deposit_apy: supply_apy,
            DBConst.borrow_apy: borrow_apy,
            DBConst.total_deposit: total_supply,
            DBConst.total_borrow: total_borrow
        }

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            health_factor: bool = False
    ):
        rpc_calls = {}
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
        if health_factor:
            rpc_calls.update(self.get_health_factor_function_info(wallet, reserves_info, block_number))
        return rpc_calls

    def get_wallet_deposit_borrow_balance(
            self,
            reserves_info,
            token_prices,
            decimals,
            deposit_amount,
            borrow_amount,
            stable_borrow_amount
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
                result[token].update({
                    "borrow_amount_in_usd": borrow_amount_in_usd,
                    "deposit_amount_in_usd": deposit_amount_in_usd,
                })
        return {self.pool_info.get("address"): result}

    def calculate_wallet_deposit_borrow_balance(
            self,
            wallet,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            pool_decimals: int = 18,
            block_number: int = 'latest',
            health_factor: bool = False
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
            borrow_amount, stable_borrow_amount
        )
        if health_factor:
            hf = self.calculate_health_factor(
                wallet, reserves_info, decoded_data, token_prices, pool_decimals, block_number)
            data.update(hf)
        return data

    # HEALTH FACTOR
    def get_health_factor_function_info(
            self,
            wallet: str,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        key = f"getUserAccountData_{self.name}_{wallet}_{block_number}".lower()
        pool_address = self.pool_info.get("address")
        rpc_calls[key] = self.state_service.get_function_info(
            pool_address, self.lending_abi, "getUserAccountData", [wallet], block_number)
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
        key = f"getUserAccountData_{self.name}_{wallet}_{block_number}".lower()
        data = decoded_data.get(key)
        health_factor = 0
        if data[0] and data[1]:
            health_factor = data[5] / 10 ** 18

        if data[0] and not data[1]:
            health_factor = 100
        return {"health_factor": health_factor}

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        reward_tokens = self.pool_info.get("rewardToken")
        if not reward_tokens:
            return {}
        rpc_calls = {}
        for token in reward_tokens:
            decimals_key = f"decimals_{token}_{block_number}".lower()
            key = f"getUserUnclaimedRewardsFromStorage_{self.name}_{wallet}_{token}_{block_number}".lower()
            rpc_calls[key] = self.get_function_rewarder_info(
                "getUserUnclaimedRewardsFromStorage", [wallet, token], block_number)
            rpc_calls[decimals_key] = self.state_service.get_function_info(
                token, ERC20_ABI, "decimals", [], block_number
            )

        return rpc_calls

    def calculate_rewards_balance(
            self,
            decoded_data: dict,
            wallet: str,
            block_number: int = "latest"):
        reward_tokens = self.pool_info.get("rewardToken")
        if not reward_tokens:
            return {}
        result = {}
        for token in reward_tokens:
            decimals_key = f"decimals_{token}_{block_number}".lower()
            key = f"getUserUnclaimedRewardsFromStorage_{self.name}_{wallet}_{token}_{block_number}".lower()
            if decoded_data.get(key) is None:
                continue
            decimals = decoded_data.get(decimals_key)
            rewards = decoded_data.get(key) / 10 ** decimals
            result.update({
                token.lower(): {"amount": rewards}
            })

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
