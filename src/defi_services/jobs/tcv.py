from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor
from defi_services.services.vault.vault_info.arbitrum.tcv_arb import TCV_VAULT_ARBITRUM

class TCV:
    def __init__(self, provider_uri, chain_id):
        self.state_processor = StateProcessor(provider_uri, chain_id)

    def get_tvl_info(
            self,
            address,
            reserves_info,
            block_number: int = "latest",
    ):
        queries = [
            {
                "query_id": "tcv-vault",
                "entity_id": "tcv-vault",
                "query_type": Query.staking_reward
            },
        ]
        res = self.state_processor.run(address, queries, block_number)
        result = res[0].get("staking_reward")
        for token, information in reserves_info.items():
            pool = information.get("pool")
            lp_token_dict = {
                pool: reserves_info[token]["poolInfo"]
            }
            dex_lp_info = self.get_lp_token_info(token, Dex.uniswap_v3, lp_token_dict)
            token_nfts = self.get_user_nft(token, Dex.uniswap_v3)
            token_info = self.get_user_info(token, Dex.uniswap_v3, token_nfts)
            token_balance = self.get_user_token_balance(token, Dex.uniswap_v3, token_info, dex_lp_info)
            tvl = {}
            for balance_info in token_balance:
                for token_id, info in balance_info['dex_user_token_balance'].items():
                    if info['token0'] not in tvl:
                        tvl[info['token0']] = 0
                    if info['token1'] not in tvl:
                        tvl[info['token1']] = 0
                    tvl[info['token0']] += info['token0_amount']
                    tvl[info['token1']] += info['token1_amount']
            result[token].update(tvl)
        return result

    def get_user_nft(self, wallet, dex_protocol):
        queries = [
            {
                'query_id': f'{dex_protocol}_usernft',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_nft
            }
        ]

        res = self.state_processor.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
        return res

    def get_user_info(self, wallet, dex_protocol, user_nfts):
        queries = [
            {
                'query_id': f'{dex_protocol}_userinfo',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_info,
                'supplied_data': {
                    'user_data': user_nfts[0][Query.dex_user_nft],
                }
            }
        ]

        res = self.state_processor.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
        return res

    def get_user_token_balance(self, wallet, dex_protocol, user_info, dex_lp_info):
        queries = [
            {
                'query_id': f'{dex_protocol}_usertokenbalance',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_token_balance,
                'supplied_data': {
                    'user_data': user_info[0][Query.dex_user_info],
                    'lp_token_info': dex_lp_info[0][Query.lp_token_info]

                }
            }
        ]

        res = self.state_processor.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
        return res

    def get_lp_token_info(self, wallet, dex_protocol, lp_token_list):
        queries = [
            {
                'query_id': f'{dex_protocol}_lptokeninfo',
                "entity_id": dex_protocol,
                'query_type': Query.lp_token_info,
                'supplied_data': {
                    'lp_token_info': lp_token_list}
            },
            {
                'query_id': f'{dex_protocol}_lptokenbalance',
                "entity_id": dex_protocol,
                'query_type': Query.token_pair_balance,
                'supplied_data': {
                    'lp_token_info': lp_token_list}
            }
        ]
        res = self.state_processor.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
        return res


