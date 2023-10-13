import json

from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/fantom",
    chain_id="0xfa"
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'granary-finance',
        "query_type": "protocol_apy"
    }
]
data = job.run('', queries, ignore_error=True)
with open('../test/apy.json', 'w') as f:
    json.dump(data, f, indent=2)
