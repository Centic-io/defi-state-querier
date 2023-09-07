from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.solana_state_processor import SolanaStateProcessor

job = SolanaStateProcessor(
    provider_uri="https://warmhearted-blue-hexagon.solana-mainnet.discover.quiknode.pro/12b82f5f8dca400ed7647980dcae7afcfa8e80cc/",
    chain_id="solana"
)
queries = [
    {
        "query_id": 1,
        "entity_id": Token.native_token,
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "DBQgYEFnW5F7ot4cgPMaXtPiv2o3VKbXJ8zz7A4pJkUS",
        "query_type": "token_balance"
    },
{
        "query_id": 3,
        "entity_id": "HpqGYp3JdD2vTR4yNhwDTpQ6d3YdREKLiRx6ELU6he8F",
        "query_type": "nft_balance"
    },
]
info = job.get_service_info()
data = job.run('DEqapWuTTDgn4RK26zC6KAQQ3DLwFFeiR6BWhBRDNVyf', queries)
print(data)