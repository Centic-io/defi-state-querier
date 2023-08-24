# defi-state-querier

### Query state data
[1] Create abi files having format like [erc20 token abi](src/abis/token/erc20_abi.py) or [aave v3 lending abi](src/abis/lending/aave_v3/aave_v3_lending_pool_abi.py).

[2] Get basic information of protocols in github or documents and save in a python file like [aave_v2_eth.py](/src/services/lending/lending_info/ethereum/aave_v2_eth.py)
**![](images/basic_information.png)** 

[3] Create file protocol service following format file [protocol_services.py](/src/services/protocol_services.py).
The service returns these data below:
- Deposit and borrow amount of wallet.
```
  {
      "<asset_address_1>": {
        "borrow_amount": 184.4,
        "deposit_amount": 331.5
      },
      "<asset_address_2>": {
        "borrow_amount": 184.4,
        "deposit_amount": 331.5
      }
   }


```
- Reward amount of wallet
```
"<asset_address_1>": {
        "deposit": {
          "rewards": {
            "<reward_address>": {
              "amount": 1.4
            }
          }
        },
        "borrow": {
          "rewards": {
            "<reward_address>": {
              "amount": 1.4
            }
          }
        }
      }

```
### Important Files