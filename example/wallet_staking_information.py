import json

from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/bsc",
    chain_id="0x38"
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'trava-vault',
        "query_type": Query.staking_reward
    }
]
data = job.run('0x53430f13A3E206c4f2375A68daeB64a087659358', queries)

with open('../test/wallet_staking.json', 'w') as f:
    json.dump(data, f, indent=2)
