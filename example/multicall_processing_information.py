import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.multi_call_state_processor import MultiCallStateProcessor
from defi_services.jobs.processors.multi_state_processor import MultiStateProcessor

# job = MultiStateProcessor(
#     provider_uri="https://rpc.ankr.com/bsc",
#     chain_id=Chain.bsc
# )
job = MultiCallStateProcessor(
    provider_uri="https://rpc.ankr.com/bsc",
    chain_id=Chain.bsc
)

queries = {
    "nft_0x72aC0daC4784d1B0F6F15cEB4eE918c40AAda55b":{
        "query_id": 1,
        "entity_id": '0x0a8901b0E25DEb55A87524f0cC164E9644020EBA',
        "query_type": Query.nft_balance,
        "wallet":"0x72aC0daC4784d1B0F6F15cEB4eE918c40AAda55b"
    },
    "token_0x00328B8a90652b37672F2f8c6c1d39CE718D7F89":{
        "query_id": 6,
        "entity_id": '0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63',
        "query_type": Query.token_balance,
        "wallet": '0x00328B8a90652b37672F2f8c6c1d39CE718D7F89'
    }
}

info = job.get_service_info()
data = job.run(queries)
print(data)

# with open('test/wepiggy.json', 'w') as f:
#     json.dump(data, f, indent=2)
