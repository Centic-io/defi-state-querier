
import json

UNITROLLER = json.loads("""
[
  {
    "constant": true,
    "inputs": [],
    "name": "pendingAdmin",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x26782247"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "newPendingAdmin",
        "type": "address"
      }
    ],
    "name": "_setPendingAdmin",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xb71d1a0c"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "comptrollerImplementation",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xbb82aa5e"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "_acceptImplementation",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xc1e80334"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "pendingComptrollerImplementation",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xdcfbc0c7"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "newPendingImplementation",
        "type": "address"
      }
    ],
    "name": "_setPendingImplementation",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xe992a041"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "_acceptAdmin",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xe9c714f2"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "admin",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xf851a440"
  },
  {
    "inputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor",
    "signature": "constructor"
  },
  {
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldPendingImplementation",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newPendingImplementation",
        "type": "address"
      }
    ],
    "name": "NewPendingImplementation",
    "type": "event",
    "signature": "0xe945ccee5d701fc83f9b8aa8ca94ea4219ec1fcbd4f4cab4f0ea57c5c3e1d815"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldImplementation",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newImplementation",
        "type": "address"
      }
    ],
    "name": "NewImplementation",
    "type": "event",
    "signature": "0xd604de94d45953f9138079ec1b82d533cb2160c906d1076d1f7ed54befbca97a"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldPendingAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newPendingAdmin",
        "type": "address"
      }
    ],
    "name": "NewPendingAdmin",
    "type": "event",
    "signature": "0xca4f2f25d0898edd99413412fb94012f9e54ec8142f9b093e7720646a95b16a9"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newAdmin",
        "type": "address"
      }
    ],
    "name": "NewAdmin",
    "type": "event",
    "signature": "0xf9ffabca9c8276e99321725bcb43fb076a6c66a54b7f21c4e8146d8519b417dc"
  },
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
    "type": "event",
    "signature": "0x45b96fe442630264581b197e84bbada861235052c5a1aadfff9ea4e40a969aa0"
  }
]
""")
        