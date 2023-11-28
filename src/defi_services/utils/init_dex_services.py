from src.defi_services.constants.entities.dex_services import DexServices
from src.defi_services.jobs.queriers.state_querier import StateQuerier
from src.defi_services.databases.mongodb_klg import MongoDB as KLG


def init_dex_services(state_querier: StateQuerier,provider_uri, mongo_klg: KLG(), chain_id: str):
    services = {}
    for protocol, value in DexServices.mapping.get(chain_id, {}).items():
        services[protocol] = value(state_querier, provider_uri, mongo_klg, chain_id)

    return services
