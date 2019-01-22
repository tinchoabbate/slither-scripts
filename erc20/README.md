# Slither scripts | ERC20 detection

Detect [ERC20](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md) interface in any Solidity smart contract using [Slither](https://github.com/trailofbits/slither).

The `erc20.py` script currently looks for:
- ERC20 functions signatures definition and visibility
- Custom modifiers in ERC20 functions
- ERC20 event signatures definition
- Visible (i.e. `public` or `external`) getters (as visible functions or `public` state variables)
- Allowance frontrunning mitigation with functions [`increaseAllowance (address, uint256)`](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/7fb90a1566d668bea8e25e9c769cf878f14e8ed3/contracts/token/ERC20/ERC20.sol#L105) and [`decreaseAllowance (address, uint256)`](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/7fb90a1566d668bea8e25e9c769cf878f14e8ed3/contracts/token/ERC20/ERC20.sol#L123)
- Function calls emitting the expected events:
    - `transfer` and `transferFrom` must emit `Transfer (address, address, uint256)`
    - `approve` must emit `Approval (address, address, uint256)`
    - `increaseAllowance` and `decreaseAllowance` should emit `Approval (address, address, uint256)`
- [Non-standard balance checks](https://github.com/sec-bit/awesome-buggy-erc20-tokens/blob/master/ERC20_token_issue_list.md#a19-approve-with-balance-verify) in `approve` function

Contracts in `test` folder are taken from [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-solidity)

## Usage
`python erc20.py <contract.sol> <contract-name>`

Example:
~~~
$ python erc20.py test/ERC20.sol ERC20
== ERC20 functions definition ==
[✓] transfer (address, uint256) -> (bool)
[✓] approve (address, uint256) -> (bool)
[✓] transferFrom (address, address, uint256) -> (bool)
[✓] allowance (address, address) -> (uint256)
[✓] balanceOf (address) -> (uint256)

== Custom modifiers ==
[✓] No custom modifiers in ERC20 functions

== ERC20 events ==
[✓] Transfer (address, address, uint256)
[✓] Approval (address, address, uint256)
[✓] transfer must emit Transfer (address, address, uint256)
[✓] approve must emit Approval (address, address, uint256)
[✓] transferFrom must emit Transfer (address, address, uint256)

== ERC20 getters ==
[✓] totalSupply () -> (uint256)
[x] decimals () -> (uint8)
[x] symbol () -> (string)
[x] name () -> (string)

== Allowance frontrunning mitigation ==
[✓] increaseAllowance (address, uint256) -> (bool)
[✓] decreaseAllowance (address, uint256) -> (bool)
[✓] increaseAllowance emits Approval (address, address, uint256)
[✓] decreaseAllowance emits Approval (address, address, uint256)

== Balance check in approve function ==
[✓] approve function should not check for sender's balance
~~~

## Limitations
Bear in mind that, currently, the script _does not verify_ that the functions found behave as expected. It just checks for matching signatures, return types, existence of custom modifiers, event emissions, among others. You still have to manually (or dynamically) test the functions to make sure they are doing the right thing.
