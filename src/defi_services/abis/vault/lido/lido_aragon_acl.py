import json

LIDO_ARAGON_ACL_ABI = json.loads('''
[
  {
    "constant": true,
    "inputs": [],
    "name": "hasInitialized",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "createBurnedPermission",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "burnPermissionManager",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "grantPermission",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "getPermissionParamsLength",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_paramsHash",
        "type": "bytes32"
      },
      {
        "name": "_who",
        "type": "address"
      },
      {
        "name": "_where",
        "type": "address"
      },
      {
        "name": "_what",
        "type": "bytes32"
      },
      {
        "name": "_how",
        "type": "uint256[]"
      }
    ],
    "name": "evalParams",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "NO_PERMISSION",
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_script",
        "type": "bytes"
      }
    ],
    "name": "getEVMScriptExecutor",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getRecoveryVault",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "CREATE_PERMISSIONS_ROLE",
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      },
      {
        "name": "_params",
        "type": "uint256[]"
      }
    ],
    "name": "grantPermissionP",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_who",
        "type": "address"
      },
      {
        "name": "_where",
        "type": "address"
      },
      {
        "name": "_what",
        "type": "bytes32"
      }
    ],
    "name": "hasPermission",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "token",
        "type": "address"
      }
    ],
    "name": "allowRecoverability",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "appId",
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getInitializationBlock",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "revokePermission",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "transferToVault",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      },
      {
        "name": "_index",
        "type": "uint256"
      }
    ],
    "name": "getPermissionParam",
    "outputs": [
      {
        "name": "",
        "type": "uint8"
      },
      {
        "name": "",
        "type": "uint8"
      },
      {
        "name": "",
        "type": "uint240"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_sender",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      },
      {
        "name": "_params",
        "type": "uint256[]"
      }
    ],
    "name": "canPerform",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getEVMScriptRegistry",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "ANY_ENTITY",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "removePermissionManager",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_newManager",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "setPermissionManager",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      }
    ],
    "name": "getPermissionManager",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_entity",
        "type": "address"
      },
      {
        "name": "_app",
        "type": "address"
      },
      {
        "name": "_role",
        "type": "bytes32"
      },
      {
        "name": "_manager",
        "type": "address"
      }
    ],
    "name": "createPermission",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_permissionsCreator",
        "type": "address"
      }
    ],
    "name": "initialize",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "EMPTY_PARAM_HASH",
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "kernel",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "isPetrified",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "BURN_ENTITY",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_who",
        "type": "address"
      },
      {
        "name": "_where",
        "type": "address"
      },
      {
        "name": "_what",
        "type": "bytes32"
      },
      {
        "name": "_how",
        "type": "uint256[]"
      }
    ],
    "name": "hasPermission",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_who",
        "type": "address"
      },
      {
        "name": "_where",
        "type": "address"
      },
      {
        "name": "_what",
        "type": "bytes32"
      },
      {
        "name": "_how",
        "type": "bytes"
      }
    ],
    "name": "hasPermission",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "entity",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "app",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "name": "allowed",
        "type": "bool"
      }
    ],
    "name": "SetPermission",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "entity",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "app",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "name": "paramsHash",
        "type": "bytes32"
      }
    ],
    "name": "SetPermissionParams",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "app",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "name": "manager",
        "type": "address"
      }
    ],
    "name": "ChangePermissionManager",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "executor",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "script",
        "type": "bytes"
      },
      {
        "indexed": false,
        "name": "input",
        "type": "bytes"
      },
      {
        "indexed": false,
        "name": "returnData",
        "type": "bytes"
      }
    ],
    "name": "ScriptResult",
    "type": "event"
  }
]
''')