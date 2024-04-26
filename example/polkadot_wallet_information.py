from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.substrate_state_processor import SubstrateStateProcessor

job = SubstrateStateProcessor(
    provider_uri="https://late-yolo-diagram.dot-mainnet.quiknode.pro/51a1aaf2372854dfd211fca3ab375e5451222be4/",
    chain_id="polkadot"
)
queries = [
    {
        "query_id": 1,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
]
info = job.get_service_info()
data = job.run('16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD', queries)
print(data)
