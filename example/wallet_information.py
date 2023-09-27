from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    # provider_uri="https://rpc.ankr.com/eth",
    # chain_id="0x1"
    provider_uri="https://arbitrum-one.publicnode.com",
    chain_id="0xa4b1"
)
queries = [
    {
        "query_id": 2,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    # {
    #     "query_id": 1,
    #     "entity_id": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    #     "query_type": "token_balance"
    # },
    {
        "query_id": 1,
        "entity_id": Lending.tenderfi,
        "query_type": "deposit_borrow"
    },
    # {
    #     "query_id": 3,
    #     "entity_id": "tenderfi",
    #     "query_type": "protocol_reward"
    # },
]
info = job.get_service_info()
data = job.run('0xa64f929a9f94bf68b50a64ea0f2e3a779fdd29a8', queries, 135038517)
print(data)
