from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.vault_constant import Vault
from defi_services.services.vault.trava_vault_services import TravaVaultStateService


class VaultServices:
    # chain
    bsc = {
        Vault.trava_vault: TravaVaultStateService
    }

    mapping = {
        Chain.bsc: bsc
    }
