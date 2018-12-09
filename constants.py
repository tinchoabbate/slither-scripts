ERC20_FX_SIGNATURES = [
    ("transfer", ["address", "uint256"], ["bool"]),
    ("transferFrom", ["address", "address", "uint256"], ["bool"]),
    ("approve", ["address", "uint256"], ["bool"]),
    ("allowance", ["address", "address"], ["uint256"]),
    ("balanceOf", ["address"], ["uint256"]),
]

ERC20_EVENT_SIGNATURES = [
    ("Transfer", ["address", "address", "uint256"]),
    ("Approval", ["address", "address", "uint256"]),
]

ERC20_GETTERS = [
    ("totalSupply", [], ["uint256"]),
    ("decimals", [], ["uint8"]),
    ("symbol", [], ["string"]),
    ("name", [], ["string"]),
]
