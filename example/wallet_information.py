import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.call_state_processor import CallStateProcessor

job = CallStateProcessor(
    provider_uri="https://rpc.ankr.com/base",
    chain_id=Chain.base
)

queries = [
    {
        "query_id": 4,
        "entity_id": 'compound_v3',
        "query_type": Query.protocol_reward
    },
    {
        "query_id": 5,
        "entity_id": 'compound-v3',
        "query_type": Query.deposit_borrow
    }
]

info = job.get_service_info()
data = job.run('0x5a2b397F50e94545369A7f246ea64090C8116FAb'.lower(), queries)
print(data)

with open('test/compound-v3-base.json', 'w') as f:
    json.dump(data, f, indent=2)
