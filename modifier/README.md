# Slither scripts | Functions by modifier

Detect functions in any set of Solidity smart contract that are labeled with a given modifier, using [Slither](https://github.com/trailofbits/slither).

This script is based on [Slither's `contract-summary` printer](https://github.com/trailofbits/slither/blob/ff280c2b6f35f8df4efff92903700da7d04fb415/slither/printers/summary/contract.py#L13).

## Usage
`python modifier.py <contract.sol> <modifier-name>`

Example:
~~~
$ python modifier.py test/TestContract.sol firstModifier
== Functions with firstModifier modifier ==

+ Contract ParentContract

+ Contract TestContract
  - From TestContract
    - withTwoModifiers(address) (public)
    - withOneModifier() (internal)
~~~

## Limitations
Currently, the script does not look for modifiers in internal calls.
For instance, in the following code snippet, `foo` will not be listed as having the `onlyOwner` modifier, even though it actually is restricted by that modifier due to the internal call to `bar()`.

~~~solidity
contract Test {
    modifier onlyOwner() { ... }

    function foo() public {
        bar();
    }
    
    function bar() public onlyOwner { ... }
}
~~~
