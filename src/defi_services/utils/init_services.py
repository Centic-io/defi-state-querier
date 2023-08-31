from defi_services.constants.entities.lending_services import LendingServices
from defi_services.jobs.state_querier import StateQuerier


def init_services(state_querier: StateQuerier, chain_id: str):
    services = {}
    for protocol, value in LendingServices.mapping.get(chain_id, {}).items():
        services[protocol] = value(state_querier, chain_id)

    return services
