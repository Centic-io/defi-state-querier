import json

LIDO_ALLOWED_RECIPIENTS_FACTORY_MULTI_TOKEN = json.loads('''
[
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "creator",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "addAllowedRecipient",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "trustedCaller",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "allowedRecipientsRegistry",
        "type": "address"
      }
    ],
    "name": "AddAllowedRecipientDeployed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "creator",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "allowedRecipientsRegistry",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "_defaultAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "addRecipientToAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "removeRecipientFromAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "setLimitParametersRoleHolders",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "updateSpentAmountRoleHolders",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "contract IBokkyPooBahsDateTimeContract",
        "name": "bokkyPooBahsDateTimeContract",
        "type": "address"
      }
    ],
    "name": "AllowedRecipientsRegistryDeployed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "creator",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "allowedTokensRegistry",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "_defaultAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "addTokenToAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "removeTokenFromAllowedListRoleHolders",
        "type": "address[]"
      }
    ],
    "name": "AllowedTokensRegistryDeployed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "creator",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "removeAllowedRecipient",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "trustedCaller",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "allowedRecipientsRegistry",
        "type": "address"
      }
    ],
    "name": "RemoveAllowedRecipientDeployed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "creator",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "topUpAllowedRecipients",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "trustedCaller",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "allowedRecipientsRegistry",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "allowedTokenssRegistry",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "finance",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "easyTrack",
        "type": "address"
      }
    ],
    "name": "TopUpAllowedRecipientsDeployed",
    "type": "event"
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
        "internalType": "contract AddAllowedRecipient",
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
        "internalType": "address",
        "name": "_defaultAdmin",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_addRecipientToAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "internalType": "address[]",
        "name": "_removeRecipientFromAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "internalType": "address[]",
        "name": "_setLimitParametersRoleHolders",
        "type": "address[]"
      },
      {
        "internalType": "address[]",
        "name": "_updateSpentAmountRoleHolders",
        "type": "address[]"
      },
      {
        "internalType": "contract IBokkyPooBahsDateTimeContract",
        "name": "_bokkyPooBahsDateTimeContract",
        "type": "address"
      }
    ],
    "name": "deployAllowedRecipientsRegistry",
    "outputs": [
      {
        "internalType": "contract AllowedRecipientsRegistry",
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
        "name": "_defaultAdmin",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_addTokensToAllowedListRoleHolders",
        "type": "address[]"
      },
      {
        "internalType": "address[]",
        "name": "_removeTokensFromAllowedListRoleHolders",
        "type": "address[]"
      }
    ],
    "name": "deployAllowedTokensRegistry",
    "outputs": [
      {
        "internalType": "contract AllowedTokensRegistry",
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
        "internalType": "address",
        "name": "_allowedRecipientsRegistry",
        "type": "address"
      }
    ],
    "name": "deployRemoveAllowedRecipient",
    "outputs": [
      {
        "internalType": "contract RemoveAllowedRecipient",
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
      },
      {
        "internalType": "address",
        "name": "_finance",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_easyTrack",
        "type": "address"
      }
    ],
    "name": "deployTopUpAllowedRecipients",
    "outputs": [
      {
        "internalType": "contract TopUpAllowedRecipients",
        "name": "topUpAllowedRecipients",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')