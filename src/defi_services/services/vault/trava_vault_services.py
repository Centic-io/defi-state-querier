import logging

from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.abis.vault.trava_vault_abi import TRAVA_VAULT_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.vault_constant import Vault
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.protocol_services import ProtocolServices
from defi_services.services.vault.vault_info.bsc.trava_bsc import TRAVA_VAULT_BSC
from defi_services.services.vault.vault_info.ethereum.trava_eth import TRAVA_VAULT_ETH
from defi_services.services.vault.vault_info.fantom.trava_ftm import TRAVA_VAULT_FTM

logger = logging.getLogger("Trava Vault State Service")


class TravaVaultInfo:
    mapping = {
        Chain.bsc: TRAVA_VAULT_BSC,
        Chain.ethereum: TRAVA_VAULT_ETH,
        Chain.fantom: TRAVA_VAULT_FTM
    }


class TravaVaultStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0x1"):
        super().__init__()
        self.name = f"{chain_id}_{Vault.trava_vault}"
        self.chain_id = chain_id
        self.pool_info = TravaVaultInfo.mapping.get(chain_id)

        self.vault_abi = TRAVA_VAULT_ABI
        self.state_service = state_service

    # BASIC FUNCTION
    def get_service_info(self):
        info = {
            Vault.trava_vault: {
                "chain_id": self.chain_id,
                "type": "vault",
                "protocol_info": self.pool_info
            }
        }
        return info

    def get_token_list(self):
        reward_token = self.pool_info.get('rewardToken')

        tokens = []
        if isinstance(reward_token, list):
            tokens += reward_token
        elif isinstance(reward_token, str):
            tokens.append(reward_token)

        for token, info in self.pool_info.get("reservesList", {}).items():
            asset_address = info['tokenIn']
            if asset_address == Token.native_token:
                tokens.append(Token.wrapped_token.get(self.chain_id))
            else:
                tokens.append(asset_address)

        tokens = list(set(tokens))
        return tokens

    # WALLET STAKING BALANCE
    def get_wallet_staking_balance_function_info(
            self,
            wallet: str,
            reserves_info: dict,
            block_number: int = "latest",
            return_reward: bool = False
    ):
        rpc_calls = {}
        for token in reserves_info:
            rpc_calls[f'balanceOf_{token}_{wallet}_{block_number}'.lower()] = self.state_service.get_function_info(
                token, ERC20_ABI, "balanceOf", [wallet], block_number=block_number)
            rpc_calls[f'decimals_{token}_{block_number}'.lower()] = self.state_service.get_function_info(
                token, ERC20_ABI, "decimals", block_number=block_number)

            if return_reward:
                query_reward_id = f'getTotalRewardsBalance_{token}_{wallet}_{block_number}'.lower()
                rpc_calls[query_reward_id] = self.state_service.get_function_info(
                    token, self.vault_abi, "getTotalRewardsBalance", [wallet], block_number=block_number)

        if return_reward:
            reward_token = self.pool_info["rewardToken"]
            rpc_calls[f'decimals_{reward_token}_{block_number}'.lower()] = self.state_service.get_function_info(
                reward_token, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def get_wallet_staking_balance(
            self,
            reserves_info: dict,
            token_prices,
            decimals,
            staking_amount,
            return_reward: bool = False,
            rewards: dict = None
    ):
        reward_token = self.pool_info['rewardToken']

        result = {}
        for token in reserves_info:
            value = reserves_info[token]
            asset_address = value['tokenIn']

            decimals_token = decimals.get(token)
            staking_amount_wallet = staking_amount.get(token) / 10 ** decimals_token
            result[token] = {
                asset_address: {
                    "staking_amount": staking_amount_wallet
                }
            }
            if return_reward:
                result[token][asset_address].update({
                    "rewards": {
                        reward_token: {'amount': rewards.get(token, 0)}
                    }
                })

            if token_prices:
                staking_amount_in_usd = staking_amount_wallet * token_prices.get(asset_address, 0)
                result[token][asset_address].update({
                    "staking_amount_in_usd": staking_amount_in_usd
                })
                if return_reward:
                    reward_amount = rewards.get(token, 0)
                    reward_in_usd = reward_amount * token_prices.get(reward_token, 0)
                    result[token][asset_address]['rewards'][reward_token].update({'value_in_usd': reward_in_usd})

        return result

    def calculate_wallet_staking_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            block_number: int = 'latest',
            return_reward: bool = False
    ):
        reward_token = self.pool_info['rewardToken']
        get_decimals_id = f"decimals_{reward_token}_{block_number}".lower()
        reward_decimals = decoded_data.get(get_decimals_id, 18)

        decimals, staking_amount, rewards = {}, {}, {}
        for token in reserves_info:
            get_user_data_id = f"balanceOf_{token}_{wallet}_{block_number}".lower()
            get_decimals_id = f"decimals_{token}_{block_number}".lower()
            staking_amount[token] = decoded_data[get_user_data_id]
            decimals[token] = decoded_data[get_decimals_id]

            if return_reward:
                get_reward_id = f"getTotalRewardsBalance_{token}_{wallet}_{block_number}".lower()
                rewards[token] = decoded_data[get_reward_id] / 10 ** reward_decimals

        data = self.get_wallet_staking_balance(
            reserves_info, token_prices, decimals, staking_amount, return_reward=return_reward, rewards=rewards)

        return data

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        rpc_calls = {}
        for token, value in reserves_info.items():
            rpc_calls[f'getTotalRewardsBalance_{token}_{wallet}_{block_number}'.lower()] = self.state_service.get_function_info(
                token, self.vault_abi, "getTotalRewardsBalance", [wallet], block_number=block_number)

        reward_token = self.pool_info["rewardToken"]
        rpc_calls[f'decimals_{reward_token}_{block_number}'.lower()] = self.state_service.get_function_info(
            reward_token, ERC20_ABI, "decimals", block_number=block_number)

        return rpc_calls

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):

        reward_token = self.pool_info['rewardToken']

        get_decimals_id = f"decimals_{reward_token}_{block_number}".lower()
        decimals = decoded_data[get_decimals_id]

        reward_amount = 0
        for token in reserves_info:
            get_reward_id = f"getTotalRewardsBalance_{token}_{wallet}_{block_number}".lower()
            reward_amount += decoded_data[get_reward_id] / 10 ** decimals

        return {
            reward_token: {"amount": reward_amount}
        }
