import json

LIDO_CURATED_STAKING_MODULE_ABI = json.loads('''
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_keysCount",
        "type": "uint256"
      },
      {
        "name": "_publicKeys",
        "type": "bytes"
      },
      {
        "name": "_signatures",
        "type": "bytes"
      }
    ],
    "name": "addSigningKeys",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getType",
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
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "clearNodeOperatorPenalty",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
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
    "inputs": [
      {
        "name": "_offset",
        "type": "uint256"
      },
      {
        "name": "_limit",
        "type": "uint256"
      }
    ],
    "name": "getNodeOperatorIds",
    "outputs": [
      {
        "name": "nodeOperatorIds",
        "type": "uint256[]"
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_offset",
        "type": "uint256"
      },
      {
        "name": "_limit",
        "type": "uint256"
      }
    ],
    "name": "getSigningKeys",
    "outputs": [
      {
        "name": "pubkeys",
        "type": "bytes"
      },
      {
        "name": "signatures",
        "type": "bytes"
      },
      {
        "name": "used",
        "type": "bool[]"
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_fromIndex",
        "type": "uint256"
      },
      {
        "name": "_keysCount",
        "type": "uint256"
      }
    ],
    "name": "removeSigningKeysOperatorBH",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "getNodeOperatorIsActive",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_name",
        "type": "string"
      }
    ],
    "name": "setNodeOperatorName",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_totalRewardShares",
        "type": "uint256"
      }
    ],
    "name": "getRewardsDistribution",
    "outputs": [
      {
        "name": "recipients",
        "type": "address[]"
      },
      {
        "name": "shares",
        "type": "uint256[]"
      },
      {
        "name": "penalized",
        "type": "bool[]"
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
        "name": "_indexFrom",
        "type": "uint256"
      },
      {
        "name": "_indexTo",
        "type": "uint256"
      }
    ],
    "name": "invalidateReadyToDepositKeysRange",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_locator",
        "type": "address"
      },
      {
        "name": "_type",
        "type": "bytes32"
      },
      {
        "name": "_stuckPenaltyDelay",
        "type": "uint256"
      }
    ],
    "name": "initialize",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_delay",
        "type": "uint256"
      }
    ],
    "name": "setStuckPenaltyDelay",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getStuckPenaltyDelay",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_index",
        "type": "uint256"
      }
    ],
    "name": "removeSigningKey",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_fromIndex",
        "type": "uint256"
      },
      {
        "name": "_keysCount",
        "type": "uint256"
      }
    ],
    "name": "removeSigningKeys",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "isOperatorPenalized",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "deactivateNodeOperator",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
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
    "name": "STAKING_ROUTER_ROLE",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_keysCount",
        "type": "uint256"
      },
      {
        "name": "_publicKeys",
        "type": "bytes"
      },
      {
        "name": "_signatures",
        "type": "bytes"
      }
    ],
    "name": "addSigningKeysOperatorBH",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
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
    "name": "getActiveNodeOperatorsCount",
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
        "name": "_name",
        "type": "string"
      },
      {
        "name": "_rewardAddress",
        "type": "address"
      }
    ],
    "name": "addNodeOperator",
    "outputs": [
      {
        "name": "id",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getContractVersion",
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
    "constant": true,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "getUnusedSigningKeyCount",
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
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "onRewardsMinted",
    "outputs": [],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "MANAGE_NODE_OPERATOR_ROLE",
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
    "inputs": [],
    "name": "onWithdrawalCredentialsChanged",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "activateNodeOperator",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_rewardAddress",
        "type": "address"
      }
    ],
    "name": "setNodeOperatorRewardAddress",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_fullInfo",
        "type": "bool"
      }
    ],
    "name": "getNodeOperator",
    "outputs": [
      {
        "name": "active",
        "type": "bool"
      },
      {
        "name": "name",
        "type": "string"
      },
      {
        "name": "rewardAddress",
        "type": "address"
      },
      {
        "name": "totalVettedValidators",
        "type": "uint64"
      },
      {
        "name": "totalExitedValidators",
        "type": "uint64"
      },
      {
        "name": "totalAddedValidators",
        "type": "uint64"
      },
      {
        "name": "totalDepositedValidators",
        "type": "uint64"
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
        "name": "_locator",
        "type": "address"
      },
      {
        "name": "_type",
        "type": "bytes32"
      },
      {
        "name": "_stuckPenaltyDelay",
        "type": "uint256"
      }
    ],
    "name": "finalizeUpgrade_v2",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getStakingModuleSummary",
    "outputs": [
      {
        "name": "totalExitedValidators",
        "type": "uint256"
      },
      {
        "name": "totalDepositedValidators",
        "type": "uint256"
      },
      {
        "name": "depositableValidatorsCount",
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
        "name": "_nodeOperatorIds",
        "type": "bytes"
      },
      {
        "name": "_exitedValidatorsCounts",
        "type": "bytes"
      }
    ],
    "name": "updateExitedValidatorsCount",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorIds",
        "type": "bytes"
      },
      {
        "name": "_stuckValidatorsCounts",
        "type": "bytes"
      }
    ],
    "name": "updateStuckValidatorsCount",
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
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_refundedValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "updateRefundedValidatorsCount",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
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
    "name": "getNodeOperatorsCount",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_isTargetLimitActive",
        "type": "bool"
      },
      {
        "name": "_targetLimit",
        "type": "uint256"
      }
    ],
    "name": "updateTargetValidatorsLimits",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_vettedSigningKeysCount",
        "type": "uint64"
      }
    ],
    "name": "setNodeOperatorStakingLimit",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "getNodeOperatorSummary",
    "outputs": [
      {
        "name": "isTargetLimitActive",
        "type": "bool"
      },
      {
        "name": "targetValidatorsCount",
        "type": "uint256"
      },
      {
        "name": "stuckValidatorsCount",
        "type": "uint256"
      },
      {
        "name": "refundedValidatorsCount",
        "type": "uint256"
      },
      {
        "name": "stuckPenaltyEndTimestamp",
        "type": "uint256"
      },
      {
        "name": "totalExitedValidators",
        "type": "uint256"
      },
      {
        "name": "totalDepositedValidators",
        "type": "uint256"
      },
      {
        "name": "depositableValidatorsCount",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_index",
        "type": "uint256"
      }
    ],
    "name": "getSigningKey",
    "outputs": [
      {
        "name": "key",
        "type": "bytes"
      },
      {
        "name": "depositSignature",
        "type": "bytes"
      },
      {
        "name": "used",
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
    "name": "MAX_NODE_OPERATOR_NAME_LENGTH",
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
        "name": "_depositsCount",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "bytes"
      }
    ],
    "name": "obtainDepositData",
    "outputs": [
      {
        "name": "publicKeys",
        "type": "bytes"
      },
      {
        "name": "signatures",
        "type": "bytes"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getKeysOpIndex",
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
    "inputs": [],
    "name": "getNonce",
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
    "name": "getLocator",
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
    "name": "SET_NODE_OPERATOR_LIMIT_ROLE",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "getTotalSigningKeyCount",
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
    "name": "MAX_STUCK_PENALTY_DELAY",
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
    "inputs": [],
    "name": "onExitedAndStuckValidatorsCountsUpdated",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "MAX_NODE_OPERATORS_COUNT",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_index",
        "type": "uint256"
      }
    ],
    "name": "removeSigningKeyOperatorBH",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_nodeOperatorId",
        "type": "uint256"
      },
      {
        "name": "_exitedValidatorsCount",
        "type": "uint256"
      },
      {
        "name": "_stuckValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "unsafeUpdateValidatorsCount",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "MANAGE_SIGNING_KEYS",
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
        "name": "_nodeOperatorId",
        "type": "uint256"
      }
    ],
    "name": "isOperatorPenaltyCleared",
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
        "indexed": false,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "name",
        "type": "string"
      },
      {
        "indexed": false,
        "name": "rewardAddress",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "stakingLimit",
        "type": "uint64"
      }
    ],
    "name": "NodeOperatorAdded",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "active",
        "type": "bool"
      }
    ],
    "name": "NodeOperatorActiveSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "name",
        "type": "string"
      }
    ],
    "name": "NodeOperatorNameSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "rewardAddress",
        "type": "address"
      }
    ],
    "name": "NodeOperatorRewardAddressSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "totalKeysTrimmed",
        "type": "uint64"
      }
    ],
    "name": "NodeOperatorTotalKeysTrimmed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "keysOpIndex",
        "type": "uint256"
      }
    ],
    "name": "KeysOpIndexSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "moduleType",
        "type": "bytes32"
      }
    ],
    "name": "StakingModuleTypeSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "rewardAddress",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "sharesAmount",
        "type": "uint256"
      }
    ],
    "name": "RewardsDistributed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "locatorAddress",
        "type": "address"
      }
    ],
    "name": "LocatorContractSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "approvedValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "VettedSigningKeysCountChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "depositedValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "DepositedSigningKeysCountChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "exitedValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "ExitedSigningKeysCountChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "totalValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "TotalSigningKeysCountChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "nonce",
        "type": "uint256"
      }
    ],
    "name": "NonceChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "stuckPenaltyDelay",
        "type": "uint256"
      }
    ],
    "name": "StuckPenaltyDelayChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "stuckValidatorsCount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "refundedValidatorsCount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "stuckPenaltyEndTimestamp",
        "type": "uint256"
      }
    ],
    "name": "StuckPenaltyStateChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "targetValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "TargetValidatorsCountChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "recipientAddress",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "sharesPenalizedAmount",
        "type": "uint256"
      }
    ],
    "name": "NodeOperatorPenalized",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "version",
        "type": "uint256"
      }
    ],
    "name": "ContractVersionSet",
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
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "vault",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "token",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "RecoverToVault",
    "type": "event"
  }
]
''')