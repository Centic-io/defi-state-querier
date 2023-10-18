class Query:
    address = "address"
    abi = "abi"
    function = "function"
    params = "params"
    block_number = "block_number"
    module = "module"

    # query types
    token_balance = 'token_balance'
    nft_balance = 'nft_balance'
    deposit_borrow = 'deposit_borrow'
    protocol_reward = 'protocol_reward'
    protocol_apy = 'protocol_apy'
    health_factor = 'health_factor'
    deposit_borrow_health_factor = 'deposit_borrow_health_factor'
    protocol_supply_borrow = 'protocol_supply_borrow'
    all = [token_balance, nft_balance, deposit_borrow, protocol_reward, protocol_apy, protocol_supply_borrow]
    balance = [nft_balance, token_balance]
    # entity_id
    token = "token"
