from signature import Signature

ERC20_FX_SIGNATURES = [
    Signature("transfer", ["address", "uint256"], ["bool"]),
    Signature("approve", ["address", "uint256"], ["bool"]),
    Signature("transferFrom", ["address", "address", "uint256"], ["bool"]),
    Signature("allowance", ["address", "address"], ["uint256"]),
    Signature("balanceOf", ["address"], ["uint256"]),
]

ERC20_EVENT_SIGNATURES = [
    Signature("Transfer", ["address", "address", "uint256"]),
    Signature("Approval", ["address", "address", "uint256"]),
]

ERC20_GETTERS = [
    Signature("totalSupply", [], ["uint256"]),
    Signature("decimals", [], ["uint8"]),
    Signature("symbol", [], ["string"]),
    Signature("name", [], ["string"]),
]

ERC20_EVENT_BY_FUNCTION = {
    "transfer": ERC20_EVENT_SIGNATURES[0],
    "approve": ERC20_EVENT_SIGNATURES[1],
    "transferFrom": ERC20_EVENT_SIGNATURES[0],
    "allowance": {},
    "balanceOf": {},
}
