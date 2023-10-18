import os
from dotenv import load_dotenv
from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.utils.logger_utils import get_logger

logger = get_logger('Test processor job')
load_dotenv()


def test_processor_job():
    providers = {
        '0x1': os.environ.get("ETHEREUM_PROVIDER"),
        '0x38': os.environ.get("BSC_PROVIDER"),
        '0x89': os.environ.get("POLYGON_PROVIDER"),
        '0xfa': os.environ.get("FANTOM_PROVIDER"),
        '0xa4b1': os.environ.get("ARBITRUM_PROVIDER"),
        '0xa': os.environ.get("OPTIMISM_PROVIDER"),
        '0xa86a': os.environ.get("AVALANCHE_PROVIDER"),
        '0x2b6653dc': os.environ.get("TRON_PROVIDER")
    }
    address = '0xf1df824419879bb8a7e758173523f88efb7af193'

    data = {}
    for chain_id, provider_uri in providers.items():
        job = StateProcessor(
            provider_uri=provider_uri,
            chain_id=chain_id
        )
        queries = []
        info = job.get_service_info()
        for p_id, p in info.items():
            if p_id not in ['token', 'nft']:
                queries.append({
                    "query_id": f'{p_id}_deposit_borrow',
                    "entity_id": p_id,
                    "query_type": "deposit_borrow",
                    "reserves_list": p.get("protocol_info", {}).get("reservesList")
                })
                queries.append({
                    "query_id": f'{p_id}_protocol_reward',
                    "entity_id": p_id,
                    "query_type": "protocol_reward",
                    "reserves_list": p.get("protocol_info", {}).get("reservesList")
                })
                queries.append({
                    "query_id": f'{p_id}_protocol_apy',
                    "entity_id": p_id,
                    "query_type": "protocol_apy",
                    "reserves_list": p.get("protocol_info", {}).get("reservesList")
                })

        error = False
        try:
            result = job.run(address, queries, batch_size=100, ignore_error=True)
            data[chain_id] = result
        except Exception as ex:
            logger.exception(ex)
            logger.error(f'Exception on chain {chain_id}')
            error = True

        assert not error


if __name__ == "__main__":
    test_processor_job()
