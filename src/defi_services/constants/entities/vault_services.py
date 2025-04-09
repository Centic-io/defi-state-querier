from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.vault_constant import Vault
from defi_services.services.vault.tcv_vault_services import TCVVaultStateService
from defi_services.services.vault.trava_vault_services import TravaVaultStateService


class VaultServices:
    # chain
    bsc = {
        Vault.trava_vault: TravaVaultStateService
    }

    ethereum = {
        Vault.trava_vault: TravaVaultStateService
    }

    fantom = {
        Vault.trava_vault: TravaVaultStateService
    }

    arbitrum = {
        Vault.tcv_vault: TCVVaultStateService
    }

    mapping = {
        Chain.bsc: bsc,
        Chain.ethereum: ethereum,
        Chain.fantom: fantom,
        Chain.arbitrum: arbitrum
    }
