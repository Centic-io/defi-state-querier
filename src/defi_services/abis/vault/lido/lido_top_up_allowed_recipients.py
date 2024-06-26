import json

LIDO_TOP_UP_RECIPIENTS_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_trustedCaller",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_allowedRecipientsRegistry",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_finance",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_token",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_easyTrack",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "allowedRecipientsRegistry",
    "outputs": [
      {
        "internalType": "contract AllowedRecipientsRegistry",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_creator",
        "type": "address"
      },
      {
        "internalType": "bytes",
        "name": "_evmScriptCallData",
        "type": "bytes"
      }
    ],
    "name": "createEVMScript",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes",
        "name": "_evmScriptCallData",
        "type": "bytes"
      }
    ],
    "name": "decodeEVMScriptCallData",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "recipients",
        "type": "address[]"
      },
      {
        "internalType": "uint256[]",
        "name": "amounts",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "easyTrack",
    "outputs": [
      {
        "internalType": "contract EasyTrack",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "finance",
    "outputs": [
      {
        "internalType": "contract IFinance",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "token",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "trustedCaller",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')