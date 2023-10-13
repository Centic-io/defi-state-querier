import json

from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/avalanche",
    chain_id="0xa86a"
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'aave-v2',
        "query_type": "protocol_apy"
    }
]
data = job.run('', queries, ignore_error=True)
with open('../test/apy.json', 'w') as f:
    json.dump(data, f, indent=2)
