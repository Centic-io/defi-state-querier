from defi_services.jobs.processors.state_processor import StateProcessor

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://fantom.publicnode.com",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"}


def test_dex_processor():
    chain_id = '0x38'
    wallet = "0x63B59cb9F03Bc57DF16d7a45423cE8148B4818D9"
    job = StateProcessor(chain_id, provider_url[chain_id])
    queries = [{
        'query_id': 'pancakeswap_lptokeninfo',
        "entity_id": 'pancake_v2',
        'query_type': 'lp_token_info',
        'version': 2
    }, {
        'query_id': 'pancakeswap_userinfo',
        "entity_id": 'pancake_v2',
        'query_type': 'user_info',
        'version': 2,
        'lp_tokens': ['0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16',
                      '0x89aB4Aceb29C95bD4D6Df3925778Ddb6268171A2']
    }]

    job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)


if __name__ == "__main__":
    test_dex_processor()
