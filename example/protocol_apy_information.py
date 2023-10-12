import json

from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/tron_jsonrpc",
    chain_id="0x2b6653dc"
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'justlend',
        "query_type": "protocol_apy"
    }
]
data = job.run('', queries)
with open('../test/apy.json', 'w') as f:
    json.dump(data, f, indent=2)
