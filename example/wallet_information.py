import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/bsc",
    chain_id=Chain.bsc
)

queries = [
    {
        "query_id": 4,
        "entity_id": 'wepiggy',
        "query_type": Query.protocol_reward
    },
    {
        "query_id": 5,
        "entity_id": 'venus',
        "query_type": Query.deposit_borrow
    },
    {
        "query_id": 6,
        "entity_id": 'venus',
        "query_type": Query.protocol_apy
    }
]
# queries = [
#     {
#         "query_id": 4,
#         "entity_id": 'wepiggy',
#         "query_type": Query.protocol_reward
#     }
# ]
info = job.get_service_info()
data = job.run('0x00328B8a90652b37672F2f8c6c1d39CE718D7F89', queries)
print(data)


# with open('test/wepiggy.json', 'w') as f:
#     json.dump(data, f, indent=2)
