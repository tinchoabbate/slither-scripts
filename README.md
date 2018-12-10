# Slither scripts

Detect [ERC20](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md) interface in any Solidity smart contract using [Slither](https://github.com/trailofbits/slither).

The `erc20.py` script currently looks for:
- Function signatures and visibility
- Event signatures
- Public getters (as visible functions or public state variables)

Contracts in `test` folder are taken from [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-solidity)

## Table of Contents
- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Slither](https://github.com/trailofbits/slither)

## Install
1. Clone this repository
2. `cd slither-scripts`
3. `pip3 install -r requirements.txt`

## Usage
`python erc20.py <contract.sol> <contract-name>`

Example:
~~~
$ python erc20.py test/ERC20.sol ERC20
== ERC20 functions ==
[✓] transfer (address, uint256) -> (bool)
[✓] transferFrom (address, address, uint256) -> (bool)
[✓] approve (address, uint256) -> (bool)
[✓] allowance (address, address) -> (uint256)
[✓] balanceOf (address) -> (uint256)

== ERC20 events ==
[✓] Transfer (address, address, uint256)
[✓] Approval (address, address, uint256)

== ERC20 getters ==
[✓] totalSupply () -> (uint256)
[x] decimals () -> (uint8)
[x] symbol () -> (string)
[x] name () -> (string)
~~~

## Maintainers
[@tinchoabbate](https://github.com/tinchoabbate)
