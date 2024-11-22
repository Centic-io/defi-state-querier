from defi_services.jobs.tcv import TCV
from defi_services.services.vault.vault_info.arbitrum.tcv_arb import TCV_VAULT_ARBITRUM

job = TCV(provider_uri="https://arbitrum-one-rpc.publicnode.com", chain_id="0xa4b1")
print(
job.get_tvl_info("0xD617E75f30a432E7ea158501f9E4fD6Ce92cD2dC", TCV_VAULT_ARBITRUM.get("reservesList"))
)