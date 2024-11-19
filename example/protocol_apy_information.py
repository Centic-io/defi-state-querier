import json

from defi_services.jobs.processors.state_processor import StateProcessor

chains = ["0xa4b1"]
lending_protocols = ["radiant-v2"]
provider_uri = ['https://nd-800-603-872.p2pify.com/e874cc3efd9e36b8b05bd16a1ab2bf2c']
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
                "query_type": "deposit_borrow"
            }
        ]
        data = job.run('0xb60e2465e1c31176dfbb32d712b226896d58b955', queries, ignore_error=True)
        # if "protocol_apy" in data:
        res.append(data)
        print("append!")
with open('../test/apy.json', 'w') as f:
    json.dump(res, f, indent=2)
