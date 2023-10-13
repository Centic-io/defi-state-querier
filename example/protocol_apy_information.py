import json

from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    # provider_uri="https://rpc.ankr.com/arbitrum",
    provider_uri="https://nd-800-603-872.p2pify.com/e874cc3efd9e36b8b05bd16a1ab2bf2c",
    chain_id="0xa4b1"
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'radiant-v2',
        "query_type": "protocol_apy"
    }
]
data = job.run('', queries, ignore_error=True)
with open('../test/apy.json', 'w') as f:
    json.dump(data, f, indent=2)
