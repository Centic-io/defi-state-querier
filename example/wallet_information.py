from defi_services.constants.token_constant import Token
from defi_services.jobs.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/eth",
    chain_id="0x1"
)
queries = [
    {
        "query_id": 4,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    {
        "query_id": 1,
        "entity_id": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "wepiggy",
        "query_type": "deposit_borrow"
    },
    {
        "query_id": 3,
        "entity_id": "wepiggy",
        "query_type": "protocol_reward"
    },
]
info = job.get_service_info()
data = job.run('0x3d4D6dA344D7629cB0899fbEC79a60F47955E6C7', queries, 18024932)
print(data)
