from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.substrate_state_processor import SubstrateStateProcessor

job = SubstrateStateProcessor(
    provider_uri="https://palpable-serene-smoke.dot-mainnet.discover.quiknode.pro/11d3e5dde99446e46f9bd58d9cee0727d2735cdf/",
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