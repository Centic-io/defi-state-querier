from collections import defaultdict

from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor


class TCV:
    def __init__(self, provider_uri, chain_id):
        self.state_processor = StateProcessor(provider_uri, chain_id)

    def get_tvl_info(
            self,
            address,
            reserves_info,
            block_number: int = "latest",
    ):
        lp_token_dict = {information["pool"]: information["poolInfo"] for information in reserves_info.values()}
        tcv_liquidity_user, dex_lp_info = self.get_tcv_liquidity_user_and_lp_token_info(
            wallet=address,
            dex_protocol=Dex.uniswap_v3, lp_token_list=lp_token_dict,
            block_number=block_number
        )

        tcv_nfts = {}
        for vault_address, liquidity_info in tcv_liquidity_user.items():
            # For optimize
            liquidity_user = liquidity_info.get('liquidity_user')
            if not liquidity_user:
                liquidity_info.update({'tvl': {}})
                continue

            vault_nft = self.get_user_nft(vault_address, Dex.uniswap_v3, block_number=block_number)
            tcv_nfts.update(vault_nft)

        nfts_info = self.get_nfts_info(address, Dex.uniswap_v3, tcv_nfts, block_number=block_number)
        user_balance = self.get_user_token_balance(address, Dex.uniswap_v3, nfts_info, dex_lp_info, block_number=block_number)

        for token_id, info in user_balance.items():
            pool_address = info['pool_address']
            addresses = [vault_address_ for vault_address_, info in reserves_info.items() if info['pool'] == pool_address]
            vault_address = addresses[0] if addresses else None

            if (not vault_address) or (vault_address not in tcv_liquidity_user):
                continue

            if tcv_liquidity_user[vault_address].get('tvl') is None:
                tcv_liquidity_user[vault_address]['tvl'] = defaultdict(lambda: 0)

            tcv_liquidity_user[vault_address]['tvl'][info['token0']] += info['token0_amount']
            tcv_liquidity_user[vault_address]['tvl'][info['token1']] += info['token1_amount']

        return tcv_liquidity_user

    def get_user_nft(self, wallet, dex_protocol, block_number: int = 'latest'):
        queries = [
            {
                'query_id': f'{dex_protocol}_{Query.dex_user_nft}',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_nft
            }
        ]

        res = self.state_processor.run(
            wallet, queries, block_number=block_number,
            batch_size=100, max_workers=8, ignore_error=True
        )
        user_nfts = res[0][Query.dex_user_nft]
        return user_nfts

    def get_nfts_info(self, wallet, dex_protocol, user_nfts, block_number: int = 'latest'):
        queries = [
            {
                'query_id': f'{dex_protocol}_{Query.dex_user_info}',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_info,
                'supplied_data': {
                    'user_data': user_nfts,
                }
            }
        ]

        res = self.state_processor.run(
            wallet, queries, block_number=block_number,
            batch_size=100, max_workers=8, ignore_error=True
        )
        nfts_info = res[0][Query.dex_user_info]
        return nfts_info

    def get_user_token_balance(self, wallet, dex_protocol, nfts_info, lp_token_info, block_number: int = 'latest'):
        queries = [
            {
                'query_id': f'{dex_protocol}_{Query.dex_user_token_balance}',
                "entity_id": dex_protocol,
                'query_type': Query.dex_user_token_balance,
                'supplied_data': {
                    'user_data': nfts_info,
                    'lp_token_info': lp_token_info
                }
            }
        ]

        res = self.state_processor.run(
            wallet, queries, block_number=block_number,
            batch_size=100, max_workers=8, ignore_error=True
        )
        user_balance = res[0][Query.dex_user_token_balance]
        return user_balance

    def get_tcv_liquidity_user_and_lp_token_info(self, wallet, dex_protocol, lp_token_list, block_number: int = 'latest'):
        queries = [
            {
                "query_id": f"tcv-vault_{Query.staking_reward}",
                "entity_id": "tcv-vault",
                "query_type": Query.staking_reward
            },
            {
                'query_id': f'{dex_protocol}_{Query.lp_token_info}',
                "entity_id": dex_protocol,
                'query_type': Query.lp_token_info,
                'supplied_data': {
                    'lp_token_info': lp_token_list
                }
            },
            # {
            #     'query_id': f'{dex_protocol}_{Query.token_pair_balance}',
            #     "entity_id": dex_protocol,
            #     'query_type': Query.token_pair_balance,
            #     'supplied_data': {
            #         'lp_token_info': lp_token_list
            #     }
            # }
        ]
        res = self.state_processor.run(
            address=wallet, queries=queries,
            block_number=block_number,
            batch_size=100, max_workers=8,
            ignore_error=True
        )
        data = {r['query_id']: r for r in res}

        tcv_liquidity_user = data.get(f'tcv-vault_{Query.staking_reward}', {}).get(Query.staking_reward)
        lp_token_info = data.get(f'{dex_protocol}_{Query.lp_token_info}', {}).get(Query.lp_token_info)
        return tcv_liquidity_user, lp_token_info
