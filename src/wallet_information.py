from defi_services.constants.token_constant import Token
from defi_services.jobs.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://mainnet.infura.io/v3/e7031702228348699215c2d112be103b",
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
        "entity_id": "spark",
        "query_type": "deposit_borrow"
    },
    # {
    #     "query_id": 3,
    #     "entity_id": "flux",
    #     "query_type": "protocol_reward"
    # },
]
info = job.get_service_info()
data = job.run('0x8667F36D23eFd27d5451ad0ff40cB96dD9491691', queries, 18017865)
print(data)