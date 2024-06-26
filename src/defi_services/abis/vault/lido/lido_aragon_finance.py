import json

LIDO_ARAGON_FINANCE_ABI = json.loads('''
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
    "constant": true,
    "inputs": [],
    "name": "CREATE_PAYMENTS_ROLE",
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
        "name": "_token",
        "type": "address"
      },
      {
        "name": "_receiver",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      },
      {
        "name": "_initialPaymentTime",
        "type": "uint64"
      },
      {
        "name": "_interval",
        "type": "uint64"
      },
      {
        "name": "_maxExecutions",
        "type": "uint64"
      },
      {
        "name": "_reference",
        "type": "string"
      }
    ],
    "name": "newScheduledPayment",
    "outputs": [
      {
        "name": "paymentId",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_paymentId",
        "type": "uint256"
      }
    ],
    "name": "executePayment",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_vault",
        "type": "address"
      },
      {
        "name": "_periodDuration",
        "type": "uint64"
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
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "removeBudget",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "getBudget",
    "outputs": [
      {
        "name": "budget",
        "type": "uint256"
      },
      {
        "name": "hasBudget",
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
        "name": "_paymentId",
        "type": "uint256"
      },
      {
        "name": "_active",
        "type": "bool"
      }
    ],
    "name": "setPaymentStatus",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_paymentId",
        "type": "uint256"
      }
    ],
    "name": "getPayment",
    "outputs": [
      {
        "name": "token",
        "type": "address"
      },
      {
        "name": "receiver",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "initialPaymentTime",
        "type": "uint64"
      },
      {
        "name": "interval",
        "type": "uint64"
      },
      {
        "name": "maxExecutions",
        "type": "uint64"
      },
      {
        "name": "inactive",
        "type": "bool"
      },
      {
        "name": "executions",
        "type": "uint64"
      },
      {
        "name": "createdBy",
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
    "inputs": [
      {
        "name": "_transactionId",
        "type": "uint256"
      }
    ],
    "name": "getTransaction",
    "outputs": [
      {
        "name": "periodId",
        "type": "uint64"
      },
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "paymentId",
        "type": "uint256"
      },
      {
        "name": "paymentExecutionNumber",
        "type": "uint64"
      },
      {
        "name": "token",
        "type": "address"
      },
      {
        "name": "entity",
        "type": "address"
      },
      {
        "name": "isIncoming",
        "type": "bool"
      },
      {
        "name": "date",
        "type": "uint64"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "CHANGE_PERIOD_ROLE",
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
    "name": "CHANGE_BUDGETS_ROLE",
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
        "name": "_paymentId",
        "type": "uint256"
      }
    ],
    "name": "receiverExecutePayment",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_periodId",
        "type": "uint64"
      }
    ],
    "name": "getPeriod",
    "outputs": [
      {
        "name": "isCurrent",
        "type": "bool"
      },
      {
        "name": "startTime",
        "type": "uint64"
      },
      {
        "name": "endTime",
        "type": "uint64"
      },
      {
        "name": "firstTransactionId",
        "type": "uint256"
      },
      {
        "name": "lastTransactionId",
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
        "name": "_periodDuration",
        "type": "uint64"
      }
    ],
    "name": "setPeriodDuration",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "periodsLength",
    "outputs": [
      {
        "name": "",
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
        "name": "_token",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "setBudget",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
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
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "recoverToVault",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "EXECUTE_PAYMENTS_ROLE",
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
    "name": "currentPeriodId",
    "outputs": [
      {
        "name": "",
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
    "constant": false,
    "inputs": [
      {
        "name": "_maxTransitions",
        "type": "uint64"
      }
    ],
    "name": "tryTransitionAccountingPeriod",
    "outputs": [
      {
        "name": "success",
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
    "name": "getPeriodDuration",
    "outputs": [
      {
        "name": "",
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
        "name": "_token",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      },
      {
        "name": "_reference",
        "type": "string"
      }
    ],
    "name": "deposit",
    "outputs": [],
    "payable": true,
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_paymentId",
        "type": "uint256"
      }
    ],
    "name": "nextPaymentTime",
    "outputs": [
      {
        "name": "",
        "type": "uint64"
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
        "name": "_periodId",
        "type": "uint64"
      },
      {
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "getPeriodTokenStatement",
    "outputs": [
      {
        "name": "expenses",
        "type": "uint256"
      },
      {
        "name": "income",
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
    "name": "paymentsNextIndex",
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
    "inputs": [
      {
        "name": "_token",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "canMakePayment",
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
    "name": "MANAGE_PAYMENTS_ROLE",
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
    "name": "transactionsNextIndex",
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
        "name": "_token",
        "type": "address"
      }
    ],
    "name": "getRemainingBudget",
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
        "name": "_token",
        "type": "address"
      },
      {
        "name": "_receiver",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      },
      {
        "name": "_reference",
        "type": "string"
      }
    ],
    "name": "newImmediatePayment",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "vault",
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
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "periodId",
        "type": "uint64"
      },
      {
        "indexed": false,
        "name": "periodStarts",
        "type": "uint64"
      },
      {
        "indexed": false,
        "name": "periodEnds",
        "type": "uint64"
      }
    ],
    "name": "NewPeriod",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "token",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "hasBudget",
        "type": "bool"
      }
    ],
    "name": "SetBudget",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "paymentId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "name": "recipient",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "maxExecutions",
        "type": "uint64"
      },
      {
        "indexed": false,
        "name": "reference",
        "type": "string"
      }
    ],
    "name": "NewPayment",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "transactionId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "incoming",
        "type": "bool"
      },
      {
        "indexed": true,
        "name": "entity",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "reference",
        "type": "string"
      }
    ],
    "name": "NewTransaction",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "paymentId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "active",
        "type": "bool"
      }
    ],
    "name": "ChangePaymentState",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "newDuration",
        "type": "uint64"
      }
    ],
    "name": "ChangePeriodDuration",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "paymentId",
        "type": "uint256"
      }
    ],
    "name": "PaymentFailure",
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