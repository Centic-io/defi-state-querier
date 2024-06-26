import json

LIDO_ALLOWED_RECIPIENTS_BUILDER_MULTI_TOKEN_TOOLING_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "contract IAllowedRecipientsFactory",
        "name": "_factory",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_admin",
        "type": "address"
      },
      {
        "internalType": "contract IEasyTrack",
        "name": "_easytrack",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_finance",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_bokkyPooBahsDateTimeContract",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "ADD_RECIPIENT_TO_ALLOWED_LIST_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "ADD_TOKEN_TO_ALLOWED_LIST_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "DEFAULT_ADMIN_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "REMOVE_RECIPIENT_FROM_ALLOWED_LIST_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "REMOVE_TOKEN_FROM_ALLOWED_LIST_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "SET_PARAMETERS_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "UPDATE_SPENT_AMOUNT_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "admin",
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
    "name": "bokkyPooBahsDateTimeContract",
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
      }
    ],
    "name": "deployAddAllowedRecipient",
    "outputs": [
      {
        "internalType": "contract IAddAllowedRecipient",
        "name": "addAllowedRecipient",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_limit",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_periodDurationMonths",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "_recipients",
        "type": "address[]"
      },
      {
        "internalType": "string[]",
        "name": "_titles",
        "type": "string[]"
      },
      {
        "internalType": "uint256",
        "name": "_spentAmount",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "_grantRightsToEVMScriptExecutor",
        "type": "bool"
      }
    ],
    "name": "deployAllowedRecipientsRegistry",
    "outputs": [
      {
        "internalType": "contract IAllowedRecipientsRegistry",
        "name": "registry",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address[]",
        "name": "_tokens",
        "type": "address[]"
      }
    ],
    "name": "deployAllowedTokensRegistry",
    "outputs": [
      {
        "internalType": "contract IAllowedTokensRegistry",
        "name": "registry",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_trustedCaller",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_limit",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_periodDurationMonths",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "_tokens",
        "type": "address[]"
      },
      {
        "internalType": "address[]",
        "name": "_recipients",
        "type": "address[]"
      },
      {
        "internalType": "string[]",
        "name": "_titles",
        "type": "string[]"
      },
      {
        "internalType": "uint256",
        "name": "_spentAmount",
        "type": "uint256"
      }
    ],
    "name": "deployFullSetup",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
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
      }
    ],
    "name": "deployRemoveAllowedRecipient",
    "outputs": [
      {
        "internalType": "contract IRemoveAllowedRecipient",
        "name": "removeAllowedRecipient",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_recipient",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "_title",
        "type": "string"
      },
      {
        "internalType": "address[]",
        "name": "_tokens",
        "type": "address[]"
      },
      {
        "internalType": "uint256",
        "name": "_limit",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_periodDurationMonths",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_spentAmount",
        "type": "uint256"
      }
    ],
    "name": "deploySingleRecipientTopUpOnlySetup",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
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
        "name": "_allowedTokensRegistry",
        "type": "address"
      }
    ],
    "name": "deployTopUpAllowedRecipients",
    "outputs": [
      {
        "internalType": "contract ITopUpAllowedRecipients",
        "name": "topUpAllowedRecipients",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "easyTrack",
    "outputs": [
      {
        "internalType": "contract IEasyTrack",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "evmScriptExecutor",
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
    "name": "factory",
    "outputs": [
      {
        "internalType": "contract IAllowedRecipientsFactory",
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