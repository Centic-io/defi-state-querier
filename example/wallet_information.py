from defi_services.jobs.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/eth",
    chain_id="0x1"
)
queries = [
    {
        "query_id": 1,
        "entity_id": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "aave-v2",
        "query_type": "deposit_borrow"
    },
    {
        "query_id": 3,
        "entity_id": "aave-v2",
        "query_type": "protocol_reward"
    },
]
info = job.get_service_info()
data = job.run('0xfe2e023bba664757aaf6b72f9b6a8cfc3ada0b28', queries, 17983787)
print(data)
