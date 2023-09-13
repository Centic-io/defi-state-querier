from defi_services.abis.lending.compound_v3.comet_abi import COMET_ABI
from defi_services.abis.lending.compound_v3.comet_ext_abi import COMET_EXT_ABI
from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
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

    # REWARDS BALANCE
    def get_claimable_rewards_balance_function_info(
            self,
            wallet_address: str,
            block_number: int = "latest",
    ):
        result = {}
        for token, value in self.pool_info.get("reservesList").items():
            ext_address = value.get("cometExt")
            rpc_call = self.state_service.get_function_info(
                ext_address, self.comet_ext, "baseTrackingAccrued", [wallet_address], block_number)
            get_reward_id = f"baseTrackingAccrued_{ext_address}_{wallet_address}_{block_number}".lower()
            result[get_reward_id] = rpc_call
        return result

    def calculate_claimable_rewards_balance(
            self, wallet_address: str, decoded_data: dict, block_number: int = "latest"):
        reward_amount = 0
        for token, value in self.pool_info.get("reservesList").items():
            ext_address = value.get("cometExt")
            get_reward_id = f"baseTrackingAccrued_{ext_address}_{wallet_address}_{block_number}".lower()
            reward_amount += decoded_data.get(get_reward_id) / 10 ** 18
        reward_token = self.pool_info.get("rewardToken")
        result = {
            reward_token: {"amount": reward_amount}
        }
        return result

    # WALLET DEPOSIT BORROW BALANCE
    def get_wallet_deposit_borrow_balance_function_info(
            self,
            wallet_address: str,
            reserves_info: dict,
            block_number: int = "latest",
            is_oracle_price: bool = False
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
            borrow_key = f"borrowBalanceOf_{comet}_{underlying}_{wallet_address}_{block_number}".lower()
            rpc_calls[borrow_key] = self.state_service.get_function_info(
                comet, self.comet_abi, "borrowBalanceOf", [wallet_address], block_number)
            for asset in assets:
                balance_key = f"collateralBalanceOf_{comet_ext}_{asset}_{wallet_address}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                rpc_calls[balance_key] = self.state_service.get_function_info(
                    comet_ext, self.comet_ext, "collateralBalanceOf", [wallet_address, asset], block_number)
                rpc_calls[decimals_key] = self.state_service.get_function_info(
                    asset, ERC20_ABI, "decimals", [], block_number
                )

        return rpc_calls

    def calculate_wallet_deposit_borrow_balance(
            self, wallet_address: str, reserves_info: dict, decoded_data: dict, token_prices: dict = None,
            wrapped_native_token_price: int = 310, block_number: int = "latest", is_oracle_price: bool = False):
        result = {}
        for token, value in reserves_info.items():
            deposit_borrow = {}
            underlying = token
            if token == Token.native_token:
                underlying = Token.wrapped_token.get(self.chain_id)
            comet = value.get('comet')
            comet_ext = value.get('comet')
            assets = value.get('assets')
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            borrow_key = f"borrowBalanceOf_{comet}_{underlying}_{wallet_address}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            borrow_amount = decoded_data[borrow_key] / 10 ** decimals
            for asset in assets:
                balance_key = f"collateralBalanceOf_{comet_ext}_{asset}_{wallet_address}_{block_number}".lower()
                decimals_key = f"decimals_{asset}_{block_number}".lower()
                decimals_token = decoded_data[decimals_key]
                deposit_amount = decoded_data[balance_key] / 10 ** decimals_token
                if asset not in deposit_borrow:
                    deposit_borrow[asset] = {
                        "borrow_amount": 0,
                        "deposit_amount": deposit_amount,
                    }
                else:
                    deposit_borrow[token]["deposit_amount"] += deposit_amount

            if underlying not in deposit_borrow:
                deposit_borrow[underlying] = {
                    "borrow_amount": borrow_amount,
                    "deposit_amount": 0
                }
            else:
                deposit_borrow[underlying]["borrow_amount"] = borrow_amount
            result[comet] = deposit_borrow
        return result


