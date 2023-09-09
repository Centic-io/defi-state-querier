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
    all = [token_balance, nft_balance, deposit_borrow, protocol_reward]

    # entity_id
    token = "token"
