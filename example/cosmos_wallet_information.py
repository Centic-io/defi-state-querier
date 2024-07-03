from defi_services.constants.network_constants import Chains
from defi_services.jobs.processors.cosmos_state_processor import CosmosStateProcessor

job = CosmosStateProcessor(lcd='https://lcd.orai.io', rest_uri="https://oraichain-rest.publicnode.com/", chain_id=Chains.oraichain)

queries = [
    {
        "query_id": 1,
        "entity_id": "orai",
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "orai1lplapmgqnelqn253stz6kmvm3ulgdaytn89a8mz9y85xq8wd684s6xl3lt",
        "query_type": "token_balance"
    },
    {
        "query_id": 3,
        "entity_id": "orai1hn8w33cqvysun2aujk5sv33tku4pgcxhhnsxmvnkfvdxagcx0p8qa4l98q",
        "query_type": "token_balance"
    },
    {
        "query_id": 4,
        "entity_id": "orai1gzvndtzceqwfymu2kqhta2jn6gmzxvzqwdgvjw",
        "query_type": "token_balance"
    }
]
address = "orai1l07l0e3r35x6uymapqvuty7tgr2suh6klc4y8c"
data = job.run(address, queries, 10, batch_size=100)
print(data)
