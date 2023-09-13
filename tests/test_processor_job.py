import json

from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.utils.logger_utils import get_logger

logger = get_logger('Test processor job')


def test_processor_job():
    providers = {
        '0x1': 'https://rpc.ankr.com/eth',
        '0x38': 'https://rpc.ankr.com/bsc',
        '0x89': 'https://rpc.ankr.com/polygon',
        '0xfa': 'https://rpc.ankr.com/fantom',
        '0xa4b1': 'https://rpc.ankr.com/arbitrum',
        '0xa': 'https://rpc.ankr.com/optimism',
        '0xa86a': 'https://rpc.ankr.com/avalanche'
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
                    "query_type": "deposit_borrow"
                })
                queries.append({
                    "query_id": f'{p_id}_protocol_reward',
                    "entity_id": p_id,
                    "query_type": "protocol_reward"
                })

        error = False
        try:
            result = job.run(address, queries, batch_size=100, ignore_error=True)
            data[chain_id] = result
        except Exception as ex:
            logger.exception(ex)
            error = True

        assert not error

    with open('tests/lib_service_data.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    test_processor_job()
