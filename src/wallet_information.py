from defi_services.constants.token_constant import Token
from defi_services.jobs.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/eth",
    chain_id="0x1"
)
queries = [
    # {
    #     "query_id": 4,
    #     "entity_id": Token.native_token,
    #     "query_type": "token_balance"
    # },
    # {
    #     "query_id": 1,
    #     "entity_id": "0x6b175474e89094c44da98b954eedeac495271d0f",
    #     "query_type": "token_balance"
    # },
    {
        "query_id": 2,
        "entity_id": "onyx",
        "query_type": "deposit_borrow"
    },
    # {
    #     "query_id": 3,
    #     "entity_id": "onyx",
    #     "query_type": "protocol_reward"
    # },
]
info = job.get_service_info()
data = job.run('0xaebb8FDBD5E52F99630cEBB80D0a1c19892EB4C2', queries, 18018070)
print(data)
