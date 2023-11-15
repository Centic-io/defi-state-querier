
import json

LEGACYJUMPRATEMODELV2 = json.loads("""
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "baseRatePerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "multiplierPerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "jumpMultiplierPerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "kink_",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "owner_",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor",
    "signature": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "baseRatePerBlock",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "multiplierPerBlock",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "jumpMultiplierPerBlock",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "kink",
        "type": "uint256"
      }
    ],
    "name": "NewInterestParams",
    "type": "event",
    "signature": "0x6960ab234c7ef4b0c9197100f5393cfcde7c453ac910a27bd2000aa1dd4c068d"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "baseRatePerBlock",
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
    "signature": "0xf14039de"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "blocksPerYear",
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
    "signature": "0xa385fb96"
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
      }
    ],
    "name": "getBorrowRate",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x15f24053"
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
    "type": "function",
    "signature": "0xb8168816"
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
    "type": "function",
    "signature": "0x2191f92a"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "jumpMultiplierPerBlock",
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
    "signature": "0xb9f9850a"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "kink",
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
    "signature": "0xfd2da339"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "multiplierPerBlock",
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
    "signature": "0x8726bb89"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "owner",
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
    "signature": "0x8da5cb5b"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "uint256",
        "name": "baseRatePerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "multiplierPerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "jumpMultiplierPerYear",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "kink_",
        "type": "uint256"
      }
    ],
    "name": "updateJumpRateModel",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x2037f3e7"
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
      }
    ],
    "name": "utilizationRate",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "pure",
    "type": "function",
    "signature": "0x6e71e2d8"
  }
]
""")
        