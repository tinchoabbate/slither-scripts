ERC20_FX_SIGNATURES = [
    {"name": "transfer", "args": ["address", "uint256"], "returns": ["bool"]},
    {"name": "approve", "args": ["address", "uint256"], "returns": ["bool"]},
    {"name": "transferFrom", "args": ["address", "address", "uint256"], "returns": ["bool"]},
    {"name": "allowance", "args": ["address", "address"], "returns": ["uint256"]},
    {"name": "balanceOf", "args": ["address"], "returns": ["uint256"]},
]

ERC20_EVENT_SIGNATURES = [
    {"name": "Transfer", "args": ["address", "address", "uint256"]},
    {"name": "Approval", "args": ["address", "address", "uint256"]},
]

ERC20_GETTERS = [
    {"name": "totalSupply", "args": [], "returns": ["uint256"]},
    {"name": "decimals", "args": [], "returns": ["uint8"]},
    {"name": "symbol", "args": [], "returns": ["string"]},
    {"name": "name", "args": [], "returns": ["string"]},
]

ERC20_EVENT_BY_FUNCTION = {
    "transfer": ERC20_EVENT_SIGNATURES[0],
    "approve": ERC20_EVENT_SIGNATURES[1],
    "transferFrom": ERC20_EVENT_SIGNATURES[0],
    "allowance": {},
    "balanceOf": {},
}
