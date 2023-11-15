
import json

COMET_CORE = json.loads("""
[
  {
    "inputs": [],
    "name": "InvalidInt104",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidInt256",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt104",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt128",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt64",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NegativeNumber",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "manager",
        "type": "address"
      }
    ],
    "name": "hasPermission",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "isAllowed",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "liquidatorPoints",
    "outputs": [
      {
        "internalType": "uint32",
        "name": "numAbsorbs",
        "type": "uint32"
      },
      {
        "internalType": "uint64",
        "name": "numAbsorbed",
        "type": "uint64"
      },
      {
        "internalType": "uint128",
        "name": "approxSpend",
        "type": "uint128"
      },
      {
        "internalType": "uint32",
        "name": "_reserved",
        "type": "uint32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "totalsCollateral",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "totalSupplyAsset",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "_reserved",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userBasic",
    "outputs": [
      {
        "internalType": "int104",
        "name": "principal",
        "type": "int104"
      },
      {
        "internalType": "uint64",
        "name": "baseTrackingIndex",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "baseTrackingAccrued",
        "type": "uint64"
      },
      {
        "internalType": "uint16",
        "name": "assetsIn",
        "type": "uint16"
      },
      {
        "internalType": "uint8",
        "name": "_reserved",
        "type": "uint8"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userCollateral",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "balance",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "_reserved",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userNonce",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
""")
        