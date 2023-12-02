
import json

ORACLE_ANCHOR = json.loads("""
[
    {
      "inputs": [
        {
          "internalType": "address[]",
          "name": "assets",
          "type": "address[]"
        },
        {
          "internalType": "address[]",
          "name": "sources",
          "type": "address[]"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "token",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "source",
          "type": "address"
        }
      ],
      "name": "AssetSourceUpdated",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [],
      "name": "OracleSystemMigrated",
      "type": "event"
    }
]
""")
        