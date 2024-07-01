from defi_services.jobs.processors.cosmos_state_processor import CosmosStateProcessor
from defi_services.services.cosmos_token_services import CosmosTokenServices

job = CosmosStateProcessor(lcd='https://cosmos-lcd.quickapi.com', rest_uri='')

queries = [
    {
        "query_id": 1,
        "entity_id": "uatom",
        "query_type": "token_balance"
    },
    {
        "query_id": 2,
        "entity_id": "ibc/0025f8a87464a471e66b234c4f93aec5b4da3d42d7986451a059273426290dd5",
        "query_type": "token_balance"
    },
    {
        "query_id": 3,
        "entity_id": "ibc/054892d6bb43af8b93aac28aa5fd7019d2c59a15dafd6f45c1fa2bf9bda22454",
        "query_type": "token_balance"
    },
    {
        "query_id": 4,
        "entity_id": "ibc/b011c1a0ad5e717f674ba59fd8e05b2f946e4fd41c9cb3311c95f7ed4b815620",
        "query_type": "token_balance"
    },
]
address = "cosmos19lcm9zhkv5qq6whp2mx47qzg0fm8ka8w8crjex"
data = job.run(address, queries)
print(data)
