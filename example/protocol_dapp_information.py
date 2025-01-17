import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.lending_constant import Lending
from defi_services.constants.entities.lending_services import LendingServices
from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.jobs.queriers.state_querier import StateQuerier

chain_id = Chain.base
protocol_id = Lending.sonne
provider_uri = "https://rpc.ankr.com/rpc"


def get_dapp_info():
    querier = StateQuerier(
        provider_uri=provider_uri
    )

    service_cls = LendingServices.mapping[chain_id][protocol_id]
    service = service_cls(
        state_service=querier,
        chain_id=chain_id
    )

    info = service.get_dapp_asset_info()

    with open(f'test/{protocol_id}_{chain_id}_info.json', 'w') as f:
        json.dump(info, f, indent=2)


def get_wallet_position():
    address = '0xDC71935f9958d643B5961f40418fC27Fb892Ea6e'
    job = StateProcessor(
        provider_uri=provider_uri,
        chain_id=chain_id
    )
    queries = [
        # {
        #     "query_id": 0,
        #     "entity_id": protocol_id,
        #     "query_type": "protocol_apy"
        # },
        {
            "query_id": 1,
            "entity_id": protocol_id,
            "query_type": "deposit_borrow"
        },
        {
            "query_id": 2,
            "entity_id": protocol_id,
            "query_type": "protocol_reward"
        }
    ]
    data = job.run(address, queries, batch_size=100, ignore_error=True)
    with open(f'test/{protocol_id}_{chain_id}_setting.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    get_wallet_position()
