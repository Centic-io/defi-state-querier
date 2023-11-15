
import json

NEWBRAVODELEGATOR = json.loads("""
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "timelock_",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "comp_",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "admin_",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "implementation_",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "votingPeriod_",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "votingDelay_",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "proposalThreshold_",
        "type": "uint256"
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
        "internalType": "address",
        "name": "oldAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
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
        "internalType": "address",
        "name": "oldImplementation",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
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
        "internalType": "address",
        "name": "oldPendingAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
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
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      }
    ],
    "name": "ProposalCanceled",
    "type": "event",
    "signature": "0x789cf55be980739dad1d0699b93b58e806b51c9d96619bfa8fe0a28abaa7b30c"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "proposer",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "targets",
        "type": "address[]"
      },
      {
        "indexed": false,
        "internalType": "uint256[]",
        "name": "values",
        "type": "uint256[]"
      },
      {
        "indexed": false,
        "internalType": "string[]",
        "name": "signatures",
        "type": "string[]"
      },
      {
        "indexed": false,
        "internalType": "bytes[]",
        "name": "calldatas",
        "type": "bytes[]"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "startBlock",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "endBlock",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "description",
        "type": "string"
      }
    ],
    "name": "ProposalCreated",
    "type": "event",
    "signature": "0x7d84a6263ae0d98d3329bd7b46bb4e8d6f98cd35a7adb45c274c8b7fd5ebd5e0"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      }
    ],
    "name": "ProposalExecuted",
    "type": "event",
    "signature": "0x712ae1383f79ac853f8d882153778e0260ef8f03b504e2866e0593e04d2b291f"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "eta",
        "type": "uint256"
      }
    ],
    "name": "ProposalQueued",
    "type": "event",
    "signature": "0x9a2e42fd6722813d69113e7d0079d3d940171428df7373df9c7f7617cfda2892"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldProposalThreshold",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newProposalThreshold",
        "type": "uint256"
      }
    ],
    "name": "ProposalThresholdSet",
    "type": "event",
    "signature": "0xccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "voter",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "proposalId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint8",
        "name": "support",
        "type": "uint8"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "votes",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "reason",
        "type": "string"
      }
    ],
    "name": "VoteCast",
    "type": "event",
    "signature": "0xb8e138887d0aa13bab447e82de9d5c1777041ecd21ca36ba824ff1e6c07ddda4"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldVotingDelay",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newVotingDelay",
        "type": "uint256"
      }
    ],
    "name": "VotingDelaySet",
    "type": "event",
    "signature": "0xc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldVotingPeriod",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newVotingPeriod",
        "type": "uint256"
      }
    ],
    "name": "VotingPeriodSet",
    "type": "event",
    "signature": "0x7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "expiration",
        "type": "uint256"
      }
    ],
    "name": "WhitelistAccountExpirationSet",
    "type": "event",
    "signature": "0x4e7b7545bc5744d0e30425959f4687475774b6c7edad77d24cb51c7d967d4515"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "oldGuardian",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "newGuardian",
        "type": "address"
      }
    ],
    "name": "WhitelistGuardianSet",
    "type": "event",
    "signature": "0x80a07e73e552148844a9c216d9724212d609cfa54e9c1a2e97203bdd2c4ad341"
  },
  {
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "address",
        "name": "implementation_",
        "type": "address"
      }
    ],
    "name": "_setImplementation",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xbb913f41"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "admin",
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
    "signature": "0xf851a440"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "implementation",
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
    "signature": "0x5c60da1b"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "pendingAdmin",
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
    "signature": "0x26782247"
  }
]
""")
        