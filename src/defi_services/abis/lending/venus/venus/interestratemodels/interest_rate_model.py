
import json

INTEREST_RATE_MODEL = json.loads("""
[
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "uint256",
        "name": "cash",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "borrows",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "reserves",
        "type": "uint256"
      }
    ],
    "name": "getBorrowRate",
    "outputs": [
      {
        "internalType": "uint256",
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
        "internalType": "uint256",
        "name": "cash",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "borrows",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "reserves",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "reserveFactorMantissa",
        "type": "uint256"
      }
    ],
    "name": "getSupplyRate",
    "outputs": [
      {
        "internalType": "uint256",
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
    "inputs": [],
    "name": "isInterestRateModel",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
""")
        