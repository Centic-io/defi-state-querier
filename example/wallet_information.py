import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.call_state_processor import CallStateProcessor
from defi_services.jobs.processors.state_processor import StateProcessor

# job = StateProcessor(
#     provider_uri="https://rpc.ankr.com/bsc",
#     chain_id=Chain.bsc
# )
job = CallStateProcessor(
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
    },
    {
        "query_id": 1,
        "entity_id": '0x55d398326f99059ff775485246999027b3197955'.lower(),
        "query_type": Query.token_balance,
        "wallet": "0x72aC0daC4784d1B0F6F15cEB4eE918c40AAda55b".lower()
    },
    {
        "query_id": 6,
        "entity_id": '0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63'.lower(),
        "query_type": Query.token_balance,
        "wallet": '0x00328B8a90652b37672F2f8c6c1d39CE718D7F89'.lower()
    }
]

info = job.get_service_info()
data = job.run('0xE0EF4E2E36f632B12a269Bb6ce722EC7Ac12E3Ac'.lower(), queries)
print(data)

# with open('test/wepiggy.json', 'w') as f:
#     json.dump(data, f, indent=2)
