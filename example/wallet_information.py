from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://evm.cronos.org/",
    chain_id="0x19"
)
queries = [
    {
        "query_id": 4,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    {
        "query_id": 1,
        "entity_id": "0x66e428c3f67a68878562e79a0234c1f83c208770",
        "query_type": "token_balance"
    }
]
info = job.get_service_info()
data = job.run('0x8995909DC0960FC9c75B6031D683124a4016825b', queries)
print(data)
