
import json

STABLECOININTERESTRATEMODEL = json.loads("""
[
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "error",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "info",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "detail",
        "type": "uint256"
      }
    ],
    "name": "Failure",
    "type": "event"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_asset",
        "type": "address"
      },
      {
        "name": "cash",
        "type": "uint256"
      },
      {
        "name": "borrows",
        "type": "uint256"
      }
    ],
    "name": "getSupplyRate",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_asset",
        "type": "address"
      },
      {
        "name": "cash",
        "type": "uint256"
      },
      {
        "name": "borrows",
        "type": "uint256"
      }
    ],
    "name": "getBorrowRate",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
""")
        