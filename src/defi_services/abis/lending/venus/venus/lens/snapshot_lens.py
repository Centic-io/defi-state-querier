
import json

SNAPSHOT_LENS = json.loads("""
[
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "comptrollerAddress",
        "type": "address"
      }
    ],
    "name": "getAccountSnapshot",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "account",
            "type": "address"
          },
          {
            "internalType": "string",
            "name": "assetName",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "vTokenAddress",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "supply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyInUsd",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateral",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowsInUsd",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "assetPrice",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accruedInterest",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "vTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRate",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isACollateral",
            "type": "bool"
          }
        ],
        "internalType": "struct SnapshotLens.AccountSnapshot[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "comptrollerAddress",
        "type": "address"
      },
      {
        "internalType": "contract VToken",
        "name": "vToken",
        "type": "address"
      }
    ],
    "name": "getAccountSnapshot",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "account",
            "type": "address"
          },
          {
            "internalType": "string",
            "name": "assetName",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "vTokenAddress",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "supply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyInUsd",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateral",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowsInUsd",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "assetPrice",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accruedInterest",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "vTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRate",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isACollateral",
            "type": "bool"
          }
        ],
        "internalType": "struct SnapshotLens.AccountSnapshot",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "comptrollerAddress",
        "type": "address"
      }
    ],
    "name": "isACollateral",
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
        