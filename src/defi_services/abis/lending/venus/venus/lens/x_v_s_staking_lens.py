
import json

X_V_S_STAKING_LENS = json.loads("""
[
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
        "name": "xvsAddress",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "xvsVaultProxyAddress",
        "type": "address"
      }
    ],
    "name": "getStakedData",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "stakedAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "pendingWithdrawalAmount",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
""")
        