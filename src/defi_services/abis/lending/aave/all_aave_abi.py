import json

from defi_services.abis.lending.aave.aave_v2.aave_incentives_controller import AAVE_INCENTIVES_CONTROLLER
from defi_services.abis.lending.aave.aave_v2.aave_oracle import AAVE_ORACLE
from defi_services.abis.lending.aave.aave_v2.avalanche_atoken import AVALANCHE_ATOKEN
from defi_services.abis.lending.aave.aave_v2.default_reserve_interest_rate_strategy import \
    DEFAULT_RESERVE_INTEREST_RATE_STRATEGY
from defi_services.abis.lending.aave.aave_v2.lending_pool import LENDING_POOL
from defi_services.abis.lending.aave.aave_v2.lending_pool_addresses_provider import LENDING_POOL_ADDRESSES_PROVIDER
from defi_services.abis.lending.aave.aave_v2.lending_pool_addresses_provider_registry import \
    LENDING_POOL_ADDRESSES_PROVIDER_REGISTRY
from defi_services.abis.lending.aave.aave_v2.lending_pool_configurator import LENDING_POOL_CONFIGURATOR
from defi_services.abis.lending.aave.aave_v2.oracle_anchor import ORACLE_ANCHOR
from defi_services.abis.lending.aave.aave_v2.stable_debt_token import STABLE_DEBT_TOKEN
from defi_services.abis.lending.aave.aave_v2.uniswap_liquidity_swap_adapter import UNISWAP_LIQUIDITY_SWAP_ADAPTER
from defi_services.abis.lending.aave.aave_v2.uniswap_repay_adapter import UNISWAP_REPAY_ADAPTER
from defi_services.abis.lending.aave.aave_v2.variable_debt_token import VARIABLE_DEBT_TOKEN
from defi_services.abis.lending.aave.aave_v2_permissioned.aave_oracle import AAVE_ORACLE_V2
from defi_services.abis.lending.aave.aave_v2_permissioned.permission_manager import PERMISSION_MANAGER
from defi_services.abis.lending.aave.aave_v3.aave_oracle import AAVE_ORACLE_V3
from defi_services.abis.lending.aave.aave_v3.aave_v3_incentives_abi import AAVE_V3_INCENTIVES_ABI
from defi_services.abis.lending.aave.aave_v3.aave_v3_lending_pool_abi import AAVE_V3_LENDING_POOL_ABI
from defi_services.abis.lending.aave.aave_v3.aave_v3_oracle_abi import AAVE_V3_ORACLE_ABI
from defi_services.abis.lending.aave.aave_v3.atoken import A_TOKEN_V3
from defi_services.abis.lending.aave.aave_v3.default_reserve_interest_rate_strategy import \
    DEFAULT_RESERVE_INTEREST_RATE_STRATEGY_V3
from defi_services.abis.lending.aave.aave_v3.pool import POOL
from defi_services.abis.lending.aave.aave_v3.pool_addresses_provider import POOL_ADDRESSES_PROVIDER
from defi_services.abis.lending.aave.aave_v3.pool_addresses_provider_registry import POOL_ADDRESSES_PROVIDER_REGISTRY
from defi_services.abis.lending.aave.aave_v3.pool_configurator import POOL_CONFIGURATOR
from defi_services.abis.lending.aave.aave_v3.price_oracle import PRICE_ORACLE
from defi_services.abis.lending.aave.aave_v3.rewards_controller import REWARDS_CONTROLLER
from defi_services.abis.lending.aave.aave_v3.stable_debt_token import STABLE_DEBT_TOKEN_V3
from defi_services.abis.lending.aave.aave_v3.variable_debt_token import VARIABLE_DEBT_TOKEN_V3


class AAVE_ABIS:
    mapping = {
        "aave_incentives_controller": AAVE_INCENTIVES_CONTROLLER,
        "aave_oracle": AAVE_ORACLE,
        "avalanche_atoken": AVALANCHE_ATOKEN,
        "default_reserve_interest_rate_strategy": DEFAULT_RESERVE_INTEREST_RATE_STRATEGY,
        "lending_pool": LENDING_POOL,
        "lending_pool_addresses_provider": LENDING_POOL_ADDRESSES_PROVIDER,
        "lending_pool_addresses_provider_registry": LENDING_POOL_ADDRESSES_PROVIDER_REGISTRY,
        "lending_pool_configurator": LENDING_POOL_CONFIGURATOR,
        "oracle_anchor": ORACLE_ANCHOR,
        "stable_debt_token": STABLE_DEBT_TOKEN,
        "uniswap_liquidity_swap_adapter": UNISWAP_LIQUIDITY_SWAP_ADAPTER,
        "uniswap_repay_adapter": UNISWAP_REPAY_ADAPTER,
        "variable_debt_token": VARIABLE_DEBT_TOKEN,
        "aave_oracle_v2": AAVE_ORACLE_V2,
        "permission_manager": PERMISSION_MANAGER,
        "aave_oracle_v3": AAVE_ORACLE_V3,
        "aave_v3_incentives_abi": AAVE_V3_INCENTIVES_ABI,
        "aave_v3_lending_pool_abi": AAVE_V3_LENDING_POOL_ABI,
        "aave_v3_oracle_abi": AAVE_V3_ORACLE_ABI,
        "a_token_v3": A_TOKEN_V3,
        "default_reserve_interest_rate_strategy_v3": DEFAULT_RESERVE_INTEREST_RATE_STRATEGY_V3,
        "pool": POOL,
        "pool_addresses_provider": POOL_ADDRESSES_PROVIDER,
        "pool_addresses_provider_registry": POOL_ADDRESSES_PROVIDER_REGISTRY,
        "pool_configurator": POOL_CONFIGURATOR,
        "price_oracle": PRICE_ORACLE,
        "rewards_controller": REWARDS_CONTROLLER,
        "stable_debt_token_v3": STABLE_DEBT_TOKEN_V3,
        "variable_debt_token_v3": VARIABLE_DEBT_TOKEN_V3,

    }

if __name__ == "__main__":
    result = []
    for key, value in AAVE_ABIS.mapping.items():
        for obj in value:
            if obj.get("type") == "event":
                if obj not in result:
                    result.append(obj)
    print(len(result))
    with open("event.json", 'w') as f:
        json.dump(result, f, indent=2)