import json

from defi_services.jobs.processors.state_processor import StateProcessor
from src.defi_services.databases.mongodb_klg import MongoDB as KLG

chain_id = '0x38'

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://rpc.ankr.com/fantom",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"}


def test_dex_processor():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor( provider_url[chain_id], chain_id)
    queries = [
        {
        'query_id': 'pancakeswap_lptokeninfo',
        "entity_id": 'pancakeswap',
        'query_type': 'lp_token_list',
    }]

    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json','w') as f:
        json.dump(res, f)

def test_lp_token_info():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor(provider_url[chain_id], chain_id)
    with open('result.json','r') as f:
        data= json.loads(f.read())
    queries = [{
        'query_id': 'spookyswap_lptokeninfo',
        "entity_id": 'pancakeswap',
        'query_type': 'lp_token_info',
        'supplied_data':{
            'lp_token_info': data[0]['lp_token_list']}
        }]
    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json','w') as f:
        json.dump(res, f)

def test_stake_token_pair():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor(provider_url[chain_id], chain_id)
    with open('result.json', 'r') as f:
        data = json.loads(f.read())
    lp_token_info= data[0]['lp_token_info']
    token_list= []
    for lp_token, info in lp_token_info.items():
        token0= info.get("token0", None)
        token1= info.get("token1", None)
        if token0 and token0 not in token_list:
            token_list.append(token0)
        if token1 and token1 not in token_list:
            token_list.append(token1)

    token_info= get_token_info(token_list)

    queries = [{
        'query_id': 'uniswapv2_lptokeninfo',
        "entity_id": 'pancakeswap',
        'query_type': 'token_pair_balance',
        'supplied_data': {
            'lp_token_info':lp_token_info,
            'token_info': token_info
            }

        }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True )
    with open('result.json', 'w') as f:
        json.dump(res, f)

def get_token_info(token_list):
    token_info={}
    mongo_klg= KLG()
    for token in token_list:
        token_data = mongo_klg.get_smart_contract(chain_id, token)
        if token_data:
            price = token_data.get("price", 0)
            decimal = token_data.get("decimals", 18)
            token_info[token] = {
                'price': price,
                'decimals': decimal}
    return token_info

def test_user_processor():
    wallet = "0xa80240eb5d7e05d3f250cf000eec0891d00b51cc"
    job = StateProcessor( provider_url[chain_id], chain_id)
    with open('result.json', 'r') as f:
        data = json.loads(f.read())
    lp_token_info= data[0]['token_pair_balance']

    token_list= []
    for lp_token, info in lp_token_info.items():
        token0= info.get("token0", None)
        token1= info.get("token1", None)
        if token0 and token0 not in token_list:
            token_list.append(token0)
        if token1 and token1 not in token_list:
            token_list.append(token1)

    token_info= get_token_info(token_list)
    queries = [
        {
        'query_id': 'pancakeswap_userinfo',
        "entity_id": 'pancakeswap',
        'query_type': 'dex_user_info',
        'supplied_data': {
            'lp_token_info': lp_token_info,
            'token_info': token_info},
        'stake': True
            }
        ,
        {
            'query_id': 'pancakeswap_userreward',
            "entity_id": 'pancakeswap',
            'query_type': 'protocol_reward',
            'supplied_data': {
                'lp_token_info': lp_token_info}

            }
        ]

    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json','w') as f:
        json.dump(res, f)

if __name__ == "__main__":
    # test_dex_processor()
    # test_lp_token_info()
    # test_stake_token_pair()
    test_user_processor()
