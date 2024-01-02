from defi_services.constants.chain_constant import Chain
from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.api.moonriver.moonbeam.network",
    chain_id=Chain.moonriver
)
queries = [
    {
        "query_id": 4,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    {
        "query_id": 1,
        "entity_id": "0x4a436073552044d5f2f49b176853ad3ad473d9d6",
        "query_type": "token_balance"
    }
]
info = job.get_service_info()
data = job.run('0x1feb8d88b56a1a743bdb8049a2f2c4826a1c1495', queries)
print(data)
