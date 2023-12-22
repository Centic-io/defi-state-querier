import json

from defi_services.jobs.processors.state_processor import StateProcessor
from src.defi_services.databases.mongodb_klg import MongoDB as KLG

chain_id = '0x1'

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://fantom.publicnode.com",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"}


def test_dex_processor():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor( provider_url[chain_id], chain_id)
    queries = [
        {
        'query_id': 'uniswap_lptokeninfo',
        "entity_id": 'uniswap_v2',
        'query_type': 'lp_token_list',
    }]

    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json','w') as f:
        json.dump(res, f)

def test_important_lp_token():
    with open('result.json', 'r') as f:
        data = json.loads(f.read())
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor(provider_url[chain_id], chain_id)
    token_info= get_token_info()
    queries = [
        {
            'query_id': 'uniswap_lptokeninfo',
            "entity_id": 'uniswap_v2',
            'query_type': 'important_lp_token_list',
            'supplied_data': { 'lp_token_list': data[0]['lp_token_list'],
                               'token_info':token_info}
            }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json', 'w') as f:
        json.dump(res, f)

def test_lp_token_info():
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor(provider_url[chain_id], chain_id)
    with open('result.json','r') as f:
        data= json.loads(f.read())
    queries = [{
        'query_id': 'uniswap_lptokeninfo',
        "entity_id": 'uniswap_v2',
        'query_type': 'lp_token_info',
        'supplied_data':data[0]['important_lp_token_list']
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
    token_info = get_token_info()

    queries = [{
        'query_id': 'uniswapv2_lptokeninfo',
        "entity_id": 'uniswap_v2',
        'query_type': 'token_pair_balance',
        'supplied_data': {
            'lp_token_info':lp_token_info,
            'token_info': token_info
            },
        }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('result.json', 'w') as f:
        json.dump(res, f)

def get_token_info():
    mongo_klg= KLG()
    res={}
    tokens= mongo_klg.get_top_1000_token(chain_id)
    for token in tokens:
        token_addr = token.get("address")
        decimals = token.get("decimals")
        price = token.get("price")
        res[token_addr]= {
            'decimals': decimals,
            'price':price
            }
    return res



if __name__ == "__main__":
    test_stake_token_pair()