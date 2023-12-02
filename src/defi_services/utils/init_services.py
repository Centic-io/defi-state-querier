from defi_services.constants.entities.dex_services import DexServices
from defi_services.constants.entities.lending_services import LendingServices
from defi_services.jobs.queriers.state_querier import StateQuerier


def init_services(state_querier: StateQuerier, chain_id: str):
    services = {}
    for protocol, value in LendingServices.mapping.get(chain_id, {}).items():
        services[protocol] = value(state_querier, chain_id)

    for protocol, value in DexServices.mapping.get(chain_id, {}).items():
        services[protocol] = value(state_querier, chain_id)

    return services
