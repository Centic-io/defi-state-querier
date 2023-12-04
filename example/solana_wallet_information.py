from defi_services.constants.token_constant import Token
from defi_services.jobs.processors.solana_state_processor import SolanaStateProcessor

job = SolanaStateProcessor(
    provider_uri="https://crimson-multi-putty.solana-mainnet.quiknode.pro/997174ce6ab5cc9d42cb037e931d18ae1a98346a/",
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
        "entity_id": "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3",
        "query_type": "token_balance"
    },
    {
        "query_id": 3,
        "entity_id": "HpqGYp3JdD2vTR4yNhwDTpQ6d3YdREKLiRx6ELU6he8F",
        "query_type": "nft_balance"
    },
]
info = job.get_service_info()
data = job.run('5cz3Jz3QnDmTsQiw5MwkfV9tq4zf2yCzWcH7tXq5BxCw', queries)
print(data)
