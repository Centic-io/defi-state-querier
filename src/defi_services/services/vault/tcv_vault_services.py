import logging

from defi_services.abis.vault.tcv_abi import TCV_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.vault_constant import Vault
from defi_services.constants.token_constant import Token
from defi_services.jobs.queriers.state_querier import StateQuerier
from defi_services.services.protocol_services import ProtocolServices
from defi_services.services.vault.vault_info.arbitrum.tcv_arb import TCV_VAULT_ARBITRUM

logger = logging.getLogger("Trava Vault State Service")


class TCVVaultInfo:
    mapping = {
        Chain.arbitrum: TCV_VAULT_ARBITRUM
    }


class TCVVaultStateService(ProtocolServices):
    def __init__(self, state_service: StateQuerier, chain_id: str = "0xa4b1"):
        super().__init__()
        self.name = f"{chain_id}_{Vault.tcv_vault}"
        self.chain_id = chain_id
        self.pool_info = TCVVaultInfo.mapping.get(chain_id)
        self.vault_abi = TCV_ABI
        self.state_service = state_service

    # BASIC FUNCTION
    def get_service_info(self):
        info = {
            Vault.tcv_vault: {
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
            rpc_calls[f'currentNow_{token}_{wallet}_{block_number}'.lower()] = self.state_service.get_function_info(
                token, TCV_ABI, "currentNow", [wallet], block_number=block_number)
            rpc_calls[f'totalLiquidityNFT_{token}_{wallet}_{block_number}'.lower()] = self.state_service.get_function_info(
                token, TCV_ABI, "totalLiquidityNFT", block_number=block_number)

        return rpc_calls

    def calculate_wallet_staking_balance(
            self,
            wallet: str,
            reserves_info: dict,
            decoded_data: dict,
            token_prices: dict,
            block_number: int = 'latest',
            return_reward: bool = False
    ):
        result = {}
        for token, information in reserves_info.items():
            liquidity_user_key = f'currentNow_{token}_{wallet}_{block_number}'.lower()
            liquidity_of_vault_key = f'totalLiquidityNFT_{token}_{wallet}_{block_number}'.lower()
            liquidity_user = decoded_data[liquidity_user_key]
            liquidity_of_vault = decoded_data[liquidity_of_vault_key]
            result[token] = {
                "liquidity_user": liquidity_user,
                "liquidity_of_vault": liquidity_of_vault
            }
        return result

    # REWARDS BALANCE
    def get_rewards_balance_function_info(
            self,
            wallet,
            reserves_info: dict = None,
            block_number: int = "latest"
    ):
        pass

    def calculate_rewards_balance(
            self, wallet: str, reserves_info: dict, decoded_data: dict, block_number: int = "latest"):
        pass
