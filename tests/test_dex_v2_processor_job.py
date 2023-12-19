import json

from defi_services.jobs.processors.state_processor import StateProcessor
from src.defi_services.databases.mongodb_klg import MongoDB as klg_mongodb

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://rpc.ankr.com/fantom",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"}


# TEST LP TOKEN INFO ##
def test_lp_token_processor(dex_protocol):
    queries = [
        {
            'query_id': f'{dex_protocol}_lptokeninfo',
            "entity_id": dex_protocol,
            'query_type': 'lp_token_list',
            'number_lp': 10
        }]

    lp_token_list = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    lp_token_inf = get_lp_token_info(lp_token_list, dex_protocol)
    lp_token_token_info = get_stake_token_pair(lp_token_inf, dex_protocol)
    with open('lp_token_info.json', 'w') as f:
        json.dump(lp_token_token_info, f)


def get_lp_token_info(data, dex_protocol):
    queries = [{
        'query_id': f'{dex_protocol}_lptokeninfo',
        "entity_id": dex_protocol,
        'query_type': 'lp_token_info',
        'supplied_data': {
            'lp_token_info': data[0]['lp_token_list']}
    }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    return res


def get_stake_token_pair(data, dex_protocol):
    lp_token_info = data[0]['lp_token_info']
    token_list = []
    for lp_token, info in lp_token_info.items():
        token0 = info.get("token0", None)
        token1 = info.get("token1", None)
        if token0 and token0 not in token_list:
            token_list.append(token0)
        if token1 and token1 not in token_list:
            token_list.append(token1)
    token_info = get_token_info(token_list)
    queries = [{
        'query_id': f'{dex_protocol}_lptokeninfo',
        "entity_id": dex_protocol,
        'query_type': 'token_pair_balance',
        'supplied_data': {
            'lp_token_info': lp_token_info,
            'token_info': token_info
        }
    }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    return res


def get_token_info(token_list):
    token_info = {}
    mongo_klg = klg_mongodb()
    for token in token_list:
        token_data = mongo_klg.get_smart_contract(chain_id, token)
        if token_data:
            price = token_data.get("price", 0)
            decimal = token_data.get("decimals", 18)
            token_info[token] = {
                'price': price,
                'decimals': decimal}
    return token_info


# TEST USER INFO ##
def test_user_info_processor(dex_protocol, list_pool: list = None):
    with open('lp_token_info.json', 'r') as f:
        data = json.loads(f.read())
    lp_token_info = data[0]['token_pair_balance']
    token_list = []
    for lp_token, info in lp_token_info.items():
        token0 = info.get("token0", None)
        token1 = info.get("token1", None)
        if token0 and token0 not in token_list:
            token_list.append(token0)
        if token1 and token1 not in token_list:
            token_list.append(token1)


    if list_pool:
        farm= {}
        pools= []
        for pool in list_pool:
            if pool in lp_token_info:
                farm.update(lp_token_info[pool])
            else:
                pools.append(pool)
        queries = [
            {
                'query_id': f'{dex_protocol}_userinfo',
                "entity_id": dex_protocol,
                'query_type': 'dex_user_info',
                'supplied_data': {
                    'lp_token_info': farm
                },
                'stake': True
            },
            {
                'query_id': f'{dex_protocol}_userinfo',
                "entity_id": dex_protocol,
                'query_type': 'dex_user_info',
                'supplied_data': {
                    'lp_token_info': pools,
                },
                'stake': False
            },
            {
                'query_id': f'{dex_protocol}_userinfo',
                "entity_id": dex_protocol,
                'query_type': 'protocol_reward',
                'supplied_data': {
                    'lp_token_info': farm}
            }
        ]
    else:
        queries = [
            {
                'query_id': f'{dex_protocol}_userinfo',
                "entity_id": dex_protocol,
                'query_type': 'dex_user_info',
                'supplied_data': {
                    'lp_token_info': lp_token_info
                },
                'stake': True
            },
            {
                'query_id': f'{dex_protocol}_userreward',
                "entity_id": dex_protocol,
                'query_type': 'protocol_reward',
                'supplied_data': {
                    'lp_token_info': lp_token_info
                }
            }
        ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json', 'w') as f:
        json.dump(res, f)


if __name__ == "__main__":
    chain_id = '0x38'
    wallet = "0x1b2a2f6ed4a1401e8c73b4c2b6172455ce2f78e8"
    job = StateProcessor(provider_url[chain_id], chain_id)
    dex_protocol= 'pancakeswap'
    # test_lp_token_processor(dex_protocol,)
    test_user_info_processor(dex_protocol)
