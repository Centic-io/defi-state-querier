import json

from defi_services.constants.chain_constant import Chain
from defi_services.jobs.processors.state_processor import StateProcessor

job = StateProcessor(
    provider_uri="https://rpc.ankr.com/eth",
    chain_id=Chain.ethereum
)

queries = [
    {
        'query_id': 'dex_user_info_sushiswap',
        'entity_id': 'sushiswap',
        'query_type': 'dex_user_info',
        'supplied_data': {
            'lp_token_info': {
                '0x99b42f2b49c395d2a77d973f6009abb5d67da343': {
                    'token0': '0x25f8087ead173b73d6e8b84329989a8eea16cf73',
                    'token1': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                    'total_supply': 7147.123213471931, 'decimals': 18,
                    'token0_amount': 744129.7772568541,
                    'token1_amount': 150.3508681821669,
                    'stake_balance': 6012.977314602618,
                    'token0_stake_amount': 627905.9670577872,
                    'token1_stake_amount': 126.10869045494897,
                    'farming_pid': 6
                }
            }
        },
        'stake': True
    },
    {
        'query_id': 'protocol_reward_sushiswap',
        'entity_id': 'sushiswap',
        'query_type': 'protocol_reward',
        'supplied_data': {
            'lp_token_info': {
                '0x99b42f2b49c395d2a77d973f6009abb5d67da343': {'token0': '0x25f8087ead173b73d6e8b84329989a8eea16cf73', 'token1': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'total_supply': 7147.123213471931, 'decimals': 18, 'token0_amount': 744129.7772568541, 'token1_amount': 150.3508681821669, 'stake_balance': 6012.977314602618, 'token0_stake_amount': 627905.9670577872, 'token1_stake_amount': 126.10869045494897, 'farming_pid': 6}
            }
        }
    }
]
# queries = [
#     {
#         "query_id": 4,
#         "entity_id": 'wepiggy',
#         "query_type": Query.protocol_reward
#     }
# ]
info = job.get_service_info()
data = job.run('0x6d16749cefb3892a101631279a8fe7369a281d0e', queries)
print(data)


with open('test/wepiggy.json', 'w') as f:
    json.dump(data, f, indent=2)
