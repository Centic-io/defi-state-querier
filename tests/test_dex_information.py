import os

from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor
from example.dex_information import provider_url
from example.dex_information_v2 import get_lp_token_list, get_lp_token_info, get_lp_token_liquidity, get_user_info, \
    get_user_reward

if not os.path.exists('test'):
    os.makedirs('test')


def test_dex_information():
    wallet = "0x89089fd89dfEdC7350861C99b71DABF4fdEA2fc0"

    for chain_id, provider_uri in provider_url.items():
        job = StateProcessor(
            provider_uri=provider_uri,
            chain_id=chain_id
        )

        info = job.get_service_info()
        for dex_id, p in info.items():
            if p['type'] == 'dex':
                error = False
                try:
                    lp_token_list = get_lp_token_list(job=job, wallet=wallet, dex_protocol=dex_id)

                    lp_token_info = {}
                    lp_token_info.update(dict(list(lp_token_list[0][Query.lp_token_list].items())[-2:]))
                    lp_token_info.update(dict(list(lp_token_list[1][Query.farming_lp_token_list].items())[-2:]))
                    assert lp_token_info, f'Missing lp of {dex_id} on chain {chain_id}'

                    get_lp_token_info(job=job, wallet=wallet, dex_protocol=dex_id)
                    get_lp_token_liquidity(job=job, wallet=wallet, dex_protocol=dex_id)
                    get_user_info(job=job, wallet=wallet, dex_protocol=dex_id)
                    get_user_reward(job=job, wallet=wallet, dex_protocol=dex_id)
                except Exception as ex:
                    print(f'Error with chain {chain_id}')
                    print(ex)
                    error = True

                assert not error, f'Fail to execute {dex_id} on chain {chain_id}'
