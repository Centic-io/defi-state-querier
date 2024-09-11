from defi_services.constants.network_constants import Chains
from defi_services.jobs.processors.ton_state_processor import TonStateProcessor

job = TonStateProcessor(provider_uri="https://toncenter.com/api/", chain_id=Chains.ton)

queries = [
    {
        "query_id": 1,
        "entity_id": "EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM__NOT",
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
        "query_type": "token_balance"
    },
    {
        "query_id": 3,
        "entity_id": "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c",
        "query_type": "token_balance"
    }
]
address = "UQD4uGNdB4a3f52mYOZf0x1nCmdd1DAvrLppL0a1cetTYCQx"
data = job.run(address, queries, 10, batch_size=100)
print(data)
