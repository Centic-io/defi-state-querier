
import json

TIMELOCK_PROTOCOL = json.loads("""
[
  {
    "constant": false,
    "inputs": [
      {
        "name": "target",
        "type": "address"
      },
      {
        "name": "value",
        "type": "uint256"
      },
      {
        "name": "signature",
        "type": "string"
      },
      {
        "name": "data",
        "type": "bytes"
      },
      {
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "executeTransaction",
    "outputs": [
      {
        "name": "",
        "type": "bytes"
      }
    ],
    "payable": true,
    "stateMutability": "payable",
    "type": "function",
    "signature": "0x0825f38f"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "acceptAdmin",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x0e18b681"
  },
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
        "name": "target",
        "type": "address"
      },
      {
        "name": "value",
        "type": "uint256"
      },
      {
        "name": "signature",
        "type": "string"
      },
      {
        "name": "data",
        "type": "bytes"
      },
      {
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "queueTransaction",
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x3a66f901"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "pendingAdmin_",
        "type": "address"
      }
    ],
    "name": "setPendingAdmin",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x4dd18bf5"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "target",
        "type": "address"
      },
      {
        "name": "value",
        "type": "uint256"
      },
      {
        "name": "signature",
        "type": "string"
      },
      {
        "name": "data",
        "type": "bytes"
      },
      {
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "cancelTransaction",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x591fcdfe"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "delay",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x6a42b8f8"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "MAXIMUM_DELAY",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x7d645fab"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "MINIMUM_DELAY",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xb1b43ae5"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "GRACE_PERIOD",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xc1a287e2"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "delay_",
        "type": "uint256"
      }
    ],
    "name": "setDelay",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xe177246e"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "name": "queuedTransactions",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0xf2b06537"
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
    "inputs": [
      {
        "name": "admin_",
        "type": "address"
      },
      {
        "name": "delay_",
        "type": "uint256"
      }
    ],
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
        "indexed": true,
        "name": "newAdmin",
        "type": "address"
      }
    ],
    "name": "NewAdmin",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "newPendingAdmin",
        "type": "address"
      }
    ],
    "name": "NewPendingAdmin",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "newDelay",
        "type": "uint256"
      }
    ],
    "name": "NewDelay",
    "type": "event",
    "signature": "0x948b1f6a42ee138b7e34058ba85a37f716d55ff25ff05a763f15bed6a04c8d2c"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "txHash",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "name": "target",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "value",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "signature",
        "type": "string"
      },
      {
        "indexed": false,
        "name": "data",
        "type": "bytes"
      },
      {
        "indexed": false,
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "CancelTransaction",
    "type": "event",
    "signature": "0x2fffc091a501fd91bfbff27141450d3acb40fb8e6d8382b243ec7a812a3aaf87"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "txHash",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "name": "target",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "value",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "signature",
        "type": "string"
      },
      {
        "indexed": false,
        "name": "data",
        "type": "bytes"
      },
      {
        "indexed": false,
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "ExecuteTransaction",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "txHash",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "name": "target",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "value",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "signature",
        "type": "string"
      },
      {
        "indexed": false,
        "name": "data",
        "type": "bytes"
      },
      {
        "indexed": false,
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "QueueTransaction",
    "type": "event"
  }
]
""")
        