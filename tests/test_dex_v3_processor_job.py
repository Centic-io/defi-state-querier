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

def test_v3():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor( provider_url[chain_id], chain_id)
    queries = [
        {
        'query_id': 'pancakeswapv3_lptokeninfo',
        "entity_id": 'pancake_v3',
        'query_type': 'lp_token_list'
    }]

    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json','w') as f:
        json.dump(res, f)
def test_user_v3():
    wallet = "0xc863ffec450e71baa242fb2efbb20f6419df0cc6"
    job = StateProcessor(provider_url[chain_id], chain_id)

    queries = [
        {
            'query_id': 'pancakeswap_userinfo',
            "entity_id": 'pancake_v3',
            'query_type': 'dex_user_nft',
            }

        ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json', 'w') as f:
        json.dump(res, f)
def test_user_info_v3():
    wallet = "0xc863ffec450e71baa242fb2efbb20f6419df0cc6"
    job = StateProcessor(provider_url[chain_id], chain_id)
    with open('user.json', 'r') as f:
        data = json.loads(f.read())
    supplied_data = data[0]['dex_user_nft']

    queries = [
        {
            'query_id': 'pancakeswap_userinfo',
            "entity_id": 'pancake_v3',
            'query_type': 'dex_user_info',
            'supplied_data': supplied_data
            }
        ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json', 'w') as f:
        json.dump(res, f)

