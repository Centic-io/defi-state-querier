from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/tron_jsonrpc",
    chain_id="0x2b6653dc"
)
queries = [
    {
        "query_id": 1,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        "query_type": "token_balance"
    },
{
        "query_id": 3,
        "entity_id": "justlend",
        "query_type": "deposit_borrow"
    },
    {
        "query_id": 4,
        "entity_id": "justlend",
        "query_type": "protocol_reward"
    },
]
info = job.get_service_info()
data = job.run('TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb', queries)
print(data)