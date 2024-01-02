import json

from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor
from src.defi_services.databases.mongodb_klg import MongoDB

chain_id = '0x1'

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://fantom.publicnode.com",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"}

wallet = "0x37A745B24eefCFd230a7ca41903E701393DDFF79"
job = StateProcessor( provider_url[chain_id], chain_id)
def get_dex_processor():

    token_info=  get_token_info()

    queries = [
        {
        'query_id': 'uniswap_v3_lptokeninfo',
        "entity_id": 'uniswap_v3',
        'query_type': Query.lp_token_list,
        'number_lp': 100,
        'supplied_data' : {"token_info":list(token_info.keys())}
    }]
    res= job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('lp_token_list.json','w') as f:
        json.dump(res, f)


def get_lp_token_info():
    # with open('lp_token_list.json', 'r') as f:
    #     data = json.loads(f.read())

    data = {"0x3416cf6c708da44db2624d63ea0aaef7113527c6": {
        "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "fee": "100"
      },
      "0x7858e59e0c01ea06df3af3d20ac7b0003275d4bf": {
        "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "fee": "500"
      },
      "0xee4cf3b78a74affa38c6a926282bcd8b5952818d": {
        "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "fee": "3000"
      }
    }
    queries = [
        {
            'query_id': 'uniswap_v3_lptokeninfo',
            "entity_id": 'uniswap_v3',
            'query_type':Query.lp_token_info,
            'supplied_data':  {
            'lp_token_info': data}
        },
            {
                'query_id': 'uniswap_v3_lptokenbalance',
                "entity_id": 'uniswap_v3',
                'query_type': Query.token_pair_balance,
                'supplied_data': {
            'lp_token_info': data}
            }
        ]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('lp_token_info.json', 'w') as f:
        json.dump(res, f)

###USER
def get_user_info():
    queries = [
        {
            'query_id': 'uniswap_v3_usernft',
            "entity_id": 'uniswap_v3',
            'query_type':Query.dex_user_nft
        }
    ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json', 'w') as f:
        json.dump(res, f)

def get_user_info_v3():
    with open('user.json', 'r') as f:
        data = json.loads(f.read())
    user_data = data[0]['dex_user_nft']

    queries = [
        {
            'query_id': 'uniswap_v3_userinfo',
            "entity_id": 'uniswap_v3',
            'query_type': 'dex_user_info',
            'supplied_data': {
                'user_data': user_data
            }
            }
        ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('user.json', 'w') as f:
        json.dump(res, f)
def get_token_info():
    mongo_klg= MongoDB()
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
    get_user_info_v3()