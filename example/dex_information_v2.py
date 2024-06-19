import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.entities.dex_info_constant import DexInfo
from defi_services.constants.network_constants import Networks, Chains
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor_multichain import StateProcessor

from defi_services.databases.mongodb_exporter import MongoExporter


def get_lp_token_list(job, wallet, dex_protocol):
    """Get all LP"""
    queries = [
        # {
        #     'query_id': f'{dex_protocol}_{Query.lp_token_list}',
        #     "entity_id": dex_protocol,
        #     'query_type': Query.lp_token_list,
        #     'number_lp': 10
        # },
        {
            'query_id': f'{dex_protocol}_{Query.farming_lp_token_list}',
            "entity_id": dex_protocol,
            'query_type': Query.farming_lp_token_list,
            'number_lp': 10
        }
    ]

    lp_token_list = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/lp_token_list.json', 'w') as f:
        json.dump(lp_token_list, f, indent=2)

    return lp_token_list


def get_lp_token_info(job, wallet, dex_protocol):
    with open('test/lp_token_list.json') as f:
        lp_token_list = json.load(f)

    queries = [
        # {
        #     'query_id': f'{dex_protocol}_{Query.lp_token_info}',
        #     "entity_id": dex_protocol,
        #     'query_type': Query.lp_token_info,
        #     'supplied_data': {
        #         'lp_token_info':  lp_token_list[0][Query.lp_token_list]
        #     }
        # },
        {
            'query_id': f'{dex_protocol}_{Query.farming_lp_token_list}',
            "entity_id": dex_protocol,
            'query_type': Query.lp_token_info,
            'supplied_data': {
                'lp_token_info': lp_token_list[0][Query.farming_lp_token_list]
            }
        }
    ]
    lp_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/lp_token_info.json', 'w') as f:
        json.dump(lp_token_info, f, indent=2)

    return lp_token_info


def get_lp_token_liquidity(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.token_pair_balance}',
            "entity_id": dex_protocol,
            'query_type': Query.token_pair_balance,
            'supplied_data': {
                'lp_token_info': lp_token_info[0][Query.lp_token_info]
            }
        }

    ]
    lp_token_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/token_pair_balance.json', 'w') as f:
        json.dump(lp_token_token_info, f, indent=2)

    return lp_token_token_info


# TEST USER INFO ##
def get_user_info(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    with open('test/token_pair_balance.json') as f:
        lp_token_liquidity_info = json.load(f)
    lp_token_liquidity_info = lp_token_liquidity_info[0][Query.token_pair_balance]

    for lp_token, info in lp_token_info.items():
        info.update(lp_token_liquidity_info[lp_token])
    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.dex_user_info}',
            "entity_id": dex_protocol,
            'query_type': Query.dex_user_info,
            'supplied_data': {
                'lp_token_info': lp_token_info
            },
            'stake': True
        }
    ]

    user_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/user_info.json', 'w') as f:
        json.dump(user_info, f, indent=2)

    return user_info


def get_user_reward(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.protocol_reward}',
            "entity_id": dex_protocol,
            'query_type': Query.protocol_reward,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]
    user_reward = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/user_reward.json', 'w') as f:
        json.dump(user_reward, f, indent=2)

    return user_reward


def export_to_mongodb(chain_id, dex_protocol):
    with open('test/lp_token_info.json', 'r') as f:
        data = json.loads(f.read())
        lp_token_info = data[0].get('lp_token_info')
    with open('test/token_pair_balance.json', 'r') as f:
        data = json.loads(f.read())
        token_pair_balance = data[0].get('token_pair_balance')

    lastest_info = []
    for lp_token, value in lp_token_info.items():
        lptoken_dict = {}
        lptoken_dict['lp_token'] = lp_token
        lptoken_dict['master_chef_address'] = DexInfo.mapping.get(chain_id).get(dex_protocol).get('master_chef_address')
        lptoken_dict['service'] = dex_protocol
        lptoken_dict.update(value)

        if lp_token in token_pair_balance:
            value2 = token_pair_balance[lp_token]
            lptoken_dict.update(value2)

        lastest_info.append(lptoken_dict)

    item_exporter = MongoExporter(collector_id='lptoken', db_prefix='', chain_id=chain_id)
    item_exporter.export_items(lastest_info)


if __name__ == "__main__":
    w = "0x025d50c11596869993b94F4bEb626eff6bEA8AAE"

    dex_ids = [Dex.sushi_v2]

    for chain_id in [Chain.ethereum]:
    # for chain_id in [Chain.bsc, Chain.ethereum, Chain.fantom, Chain.polygon, Chain.arbitrum, Chain.avalanche]:
        for dex_id in dex_ids:
            try:
                provider_url = Networks.archive_node.get(Chains.names[chain_id])
                job_ = StateProcessor(provider_url, chain_id)
                if dex_id in job_.services:
                    get_lp_token_list(job=job_, wallet=w, dex_protocol=dex_id)
                    get_lp_token_info(job=job_, wallet=w, dex_protocol=dex_id)
                    get_lp_token_liquidity(job=job_, wallet=w, dex_protocol=dex_id)
                    get_user_info(job=job_, wallet=w, dex_protocol=dex_id)
                    get_user_reward(job=job_, wallet=w, dex_protocol=dex_id)
                    # export_to_mongodb(chain_id, dex_id)
                    print(f'export {dex_id}  in {chain_id}')
            except Exception as ex:
                print(f'Error with chain {chain_id}')
                raise ex
