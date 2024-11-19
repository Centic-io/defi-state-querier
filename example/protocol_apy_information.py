import json

from defi_services.jobs.processors.state_processor import StateProcessor

chains = ["0x38", '0x1', '0xfa', '0xa', '0xa4b1', '0xa86a', '0x89']
lending_protocols = ["venus", "aave-v2", "aave-v3", "justlend", "compound-v3", "compound", "spark", 'morpho-compound',
                     'morpho-aave', 'morpho-aavev3', "radiant-v2"]
provider_uri = ['https://bsc-dataseed3.binance.org/',
                "https://rpc.ankr.com/eth",
                "https://fantom.publicnode.com",
                "https://optimism.llamarpc.com",
                "https://rpc.ankr.com/arbitrum",
                "https://rpc.ankr.com/avalanche",
                "https://rpc.ankr.com/polygon"]
res = []
for ind, chain_id in enumerate(chains):
    for entity in lending_protocols:
        job = StateProcessor(
            provider_uri=provider_uri[ind],
            chain_id=chain_id
        )
        queries = [
            {
                "query_id": chain_id,
                "entity_id": entity,
                "query_type": "protocol_apy"
            }
        ]
        data = job.run('', queries, ignore_error=True)
        # if "protocol_apy" in data:
        res.append(data)
        print("append!")
with open('../test/apy.json', 'w') as f:
    json.dump(res, f, indent=2)
