import json

from defi_services.abis.lending.venus.abi.comptroller_defi import COMPTROLLER_DEFI
from defi_services.abis.lending.venus.abi.comptrollerbeacon import COMPTROLLERBEACON
from defi_services.abis.lending.venus.abi.comptrollerimpl import COMPTROLLERIMPL
from defi_services.abis.lending.venus.abi.defaultproxyadmin import DEFAULTPROXYADMIN
from defi_services.abis.lending.venus.abi.jumpratemodelv2 import JUMPRATEMODELV2
from defi_services.abis.lending.venus.abi.poollens import POOLLENS
from defi_services.abis.lending.venus.abi.poolregistry import POOLREGISTRY
from defi_services.abis.lending.venus.abi.poolregistry_implementation import POOLREGISTRY_IMPLEMENTATION
from defi_services.abis.lending.venus.abi.poolregistry_proxy import POOLREGISTRY_PROXY
from defi_services.abis.lending.venus.abi.protocolsharereserve import PROTOCOLSHARERESERVE
from defi_services.abis.lending.venus.abi.protocolsharereserve_implementation import PROTOCOLSHARERESERVE_IMPLEMENTATION
from defi_services.abis.lending.venus.abi.protocolsharereserve_proxy import PROTOCOLSHARERESERVE_PROXY
from defi_services.abis.lending.venus.abi.rewardsdistributor_defi import REWARDSDISTRIBUTOR_DEFI_0
from defi_services.abis.lending.venus.abi.rewardsdistributorimpl import REWARDSDISTRIBUTORIMPL
from defi_services.abis.lending.venus.abi.riskfund import RISKFUND
from defi_services.abis.lending.venus.abi.riskfund_implementation import RISKFUND_IMPLEMENTATION
from defi_services.abis.lending.venus.abi.riskfund_proxy import RISKFUND_PROXY
from defi_services.abis.lending.venus.abi.shortfall import SHORTFALL
from defi_services.abis.lending.venus.abi.shortfall_implementation import SHORTFALL_IMPLEMENTATION
from defi_services.abis.lending.venus.abi.shortfall_proxy import SHORTFALL_PROXY
from defi_services.abis.lending.venus.abi.swaprouter_defi import SWAPROUTER_DEFI
from defi_services.abis.lending.venus.abi.vtokenbeacon import VTOKENBEACON
from defi_services.abis.lending.venus.abi.vtokenimpl import VTOKENIMPL
from defi_services.abis.lending.venus.governance.access_control_manager import ACCESS_CONTROL_MANAGER
from defi_services.abis.lending.venus.governance.access_controlled_v5 import ACCESS_CONTROLLED_V5
from defi_services.abis.lending.venus.governance.access_controlled_v8 import ACCESS_CONTROLLED_V8
from defi_services.abis.lending.venus.governance.governor_bravo_delegate import GOVERNOR_BRAVO_DELEGATE
from defi_services.abis.lending.venus.governance.governor_bravo_delegator import GOVERNOR_BRAVO_DELEGATOR
from defi_services.abis.lending.venus.governance.governor_bravo_events import GOVERNOR_BRAVO_EVENTS
from defi_services.abis.lending.venus.governance.timelock import TIMELOCK
from defi_services.abis.lending.venus.venus.admin.v_b_n_b_admin import V_B_N_B_ADMIN
from defi_services.abis.lending.venus.venus.comptroller.diamond import DIAMOND
from defi_services.abis.lending.venus.venus.comptroller.diamond_consolidated import DIAMOND_CONSOLIDATED
from defi_services.abis.lending.venus.venus.comptroller.facet_base import FACET_BASE
from defi_services.abis.lending.venus.venus.comptroller.market_facet import MARKET_FACET
from defi_services.abis.lending.venus.venus.comptroller.policy_facet import POLICY_FACET
from defi_services.abis.lending.venus.venus.comptroller.reward_facet import REWARD_FACET
from defi_services.abis.lending.venus.venus.comptroller.setter_facet import SETTER_FACET
from defi_services.abis.lending.venus.venus.comptroller.unitroller import UNITROLLER
from defi_services.abis.lending.venus.venus.comptroller.x_v_s_rewards_helper import X_V_S_REWARDS_HELPER
from defi_services.abis.lending.venus.venus.delegateborrowers.swap_debt_delegate import SWAP_DEBT_DELEGATE
from defi_services.abis.lending.venus.venus.governance.v_treasury import V_TREASURY
from defi_services.abis.lending.venus.venus.interestratemodels.interest_rate_model import INTEREST_RATE_MODEL
from defi_services.abis.lending.venus.venus.interestratemodels.jump_rate_model import JUMP_RATE_MODEL
from defi_services.abis.lending.venus.venus.interestratemodels.white_paper_interest_rate_model import \
    WHITE_PAPER_INTEREST_RATE_MODEL
from defi_services.abis.lending.venus.venus.lens.comptroller_lens import COMPTROLLER_LENS
from defi_services.abis.lending.venus.venus.lens.snapshot_lens import SNAPSHOT_LENS
from defi_services.abis.lending.venus.venus.lens.venus_lens import VENUS_LENS
from defi_services.abis.lending.venus.venus.lens.x_v_s_staking_lens import X_V_S_STAKING_LENS
from defi_services.abis.lending.venus.venus.liquidator.b_u_s_d_liquidator import B_U_S_D_LIQUIDATOR
from defi_services.abis.lending.venus.venus.liquidator.liquidator import LIQUIDATOR
from defi_services.abis.lending.venus.venus.oracle.price_oracle import PRICE_ORACLE
from defi_services.abis.lending.venus.venus.pegstability.peg_stability import PEG_STABILITY
from defi_services.abis.lending.venus.venus.tokens.v_a_i import V_A_I
from defi_services.abis.lending.venus.venus.tokens.v_a_i_controller import V_A_I_CONTROLLER
from defi_services.abis.lending.venus.venus.tokens.v_a_i_unitroller import V_A_I_UNITROLLER
from defi_services.abis.lending.venus.venus.tokens.v_bep20 import V_BEP20
from defi_services.abis.lending.venus.venus.tokens.v_bep20_delegate import V_BEP20_DELEGATE
from defi_services.abis.lending.venus.venus.tokens.v_bep20_delegator import V_BEP20_DELEGATOR
from defi_services.abis.lending.venus.venus.tokens.v_bep20_immutable import V_BEP20_IMMUTABLE
from defi_services.abis.lending.venus.venus.tokens.v_r_t import V_R_T
from defi_services.abis.lending.venus.venus.tokens.v_r_t_converter import V_R_T_CONVERTER
from defi_services.abis.lending.venus.venus.tokens.v_r_t_converter_proxy import V_R_T_CONVERTER_PROXY
from defi_services.abis.lending.venus.venus.tokens.v_token import V_TOKEN
from defi_services.abis.lending.venus.venus.tokens.x_v_s import X_V_S
from defi_services.abis.lending.venus.venus.tokens.x_v_s_vesting import X_V_S_VESTING
from defi_services.abis.lending.venus.venus.tokens.x_v_s_vesting_proxy import X_V_S_VESTING_PROXY
from defi_services.abis.lending.venus.venus.vault.v_a_i_vault import V_A_I_VAULT
from defi_services.abis.lending.venus.venus.vault.v_a_i_vault_proxy import V_A_I_VAULT_PROXY
from defi_services.abis.lending.venus.venus.vrtvault.v_r_t_vault import V_R_T_VAULT
from defi_services.abis.lending.venus.venus.vrtvault.v_r_t_vault_proxy import V_R_T_VAULT_PROXY
from defi_services.abis.lending.venus.venus.xvsvault.x_v_s_vault import X_V_S_VAULT
from defi_services.abis.lending.venus.venus.xvsvault.x_v_s_vault_error_reporter import X_V_S_VAULT_ERROR_REPORTER
from defi_services.abis.lending.venus.venus.xvsvault.x_v_s_vault_proxy import X_V_S_VAULT_PROXY
from defi_services.abis.lending.venus.venus_comptroller_abi import VENUS_COMPTROLLER_ABI


class VENUS_ABIS:
    mapping = [
        VENUS_COMPTROLLER_ABI,
        COMPTROLLER_DEFI,
        COMPTROLLERBEACON,
        COMPTROLLERIMPL,
        DEFAULTPROXYADMIN,
        JUMPRATEMODELV2,
        POOLLENS,
        POOLREGISTRY,
        POOLREGISTRY_IMPLEMENTATION,
        POOLREGISTRY_PROXY,
        PROTOCOLSHARERESERVE,
        PROTOCOLSHARERESERVE_IMPLEMENTATION,
        PROTOCOLSHARERESERVE_PROXY,
        REWARDSDISTRIBUTOR_DEFI_0,
        REWARDSDISTRIBUTORIMPL,
        RISKFUND,
        RISKFUND_IMPLEMENTATION,
        RISKFUND_PROXY,
        SHORTFALL,
        SHORTFALL_IMPLEMENTATION,
        SHORTFALL_PROXY,
        SWAPROUTER_DEFI,
        VTOKENBEACON,
        VTOKENIMPL,
        ACCESS_CONTROL_MANAGER,
        ACCESS_CONTROLLED_V5,
        ACCESS_CONTROLLED_V8,
        GOVERNOR_BRAVO_DELEGATOR,
        GOVERNOR_BRAVO_DELEGATE,
        GOVERNOR_BRAVO_EVENTS,
        TIMELOCK,
        V_B_N_B_ADMIN,
        DIAMOND,
        DIAMOND_CONSOLIDATED,
        FACET_BASE,
        MARKET_FACET,
        POLICY_FACET,
        REWARD_FACET,
        SETTER_FACET,
        UNITROLLER,
        X_V_S_REWARDS_HELPER,
        SWAP_DEBT_DELEGATE,
        V_TREASURY,
        INTEREST_RATE_MODEL,
        JUMP_RATE_MODEL,
        WHITE_PAPER_INTEREST_RATE_MODEL,
        COMPTROLLER_LENS,
        SNAPSHOT_LENS,
        VENUS_LENS,
        X_V_S_STAKING_LENS,
        B_U_S_D_LIQUIDATOR,
        LIQUIDATOR,
        PRICE_ORACLE,
        PEG_STABILITY,
        V_A_I,
        V_A_I_CONTROLLER,
        V_A_I_UNITROLLER,
        V_BEP20,
        V_BEP20_DELEGATE,
        V_BEP20_DELEGATOR,
        V_BEP20_IMMUTABLE,
        V_R_T,
        V_R_T_CONVERTER,
        V_R_T_CONVERTER_PROXY,
        V_TOKEN,
        X_V_S,
        X_V_S_VESTING,
        X_V_S_VESTING_PROXY,
        V_A_I_VAULT,
        V_A_I_VAULT_PROXY,
        V_R_T_VAULT,
        V_R_T_VAULT_PROXY,
        X_V_S_VAULT,
        X_V_S_VAULT_ERROR_REPORTER,
        X_V_S_VAULT_PROXY
    ]

if __name__ == "__main__":
    result = []
    for i in VENUS_ABIS.mapping:
        for obj in i:
            if obj.get('type') == "event":
                if "signature" in obj:
                    del obj['signature']
                result.append(obj)
    with open("events.json", 'w') as f:
        json.dump(result, f, indent=2)