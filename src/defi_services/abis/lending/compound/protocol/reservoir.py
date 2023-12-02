
import json

RESERVOIR = json.loads("""
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "dripRate_",
        "type": "uint256"
      },
      {
        "internalType": "contract EIP20Interface",
        "name": "token_",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "target_",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor",
    "signature": "constructor"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "drip",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x9f678cca"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "dripRate",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xd3261592"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "dripStart",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x88a91a8a"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "dripped",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x95f632b3"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "target",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xd4b83992"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "token",
    "outputs": [
      {
        "internalType": "contract EIP20Interface",
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xfc0c546a"
  }
]
""")
        