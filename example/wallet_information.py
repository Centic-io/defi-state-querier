from defi_services.constants.chain_constant import Chain
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/eth",
    chain_id=Chain.ethereum
)
queries = [
    {
        "query_id": 4,
        "entity_id": 'compound',
        "query_type": Query.deposit_borrow
    }
]
info = job.get_service_info()
data = job.run('0x23291905585578f57e155def1fc5cd66dd00db4e', queries)
print(data)
