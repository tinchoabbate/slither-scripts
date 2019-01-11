pragma solidity ^0.4.25;

contract ParentContract {
    modifier parentModifier() {
        _;
    }

    function withOneModifier() internal parentModifier { }

    function parentWithNoModifier() public {}
}

contract TestContract is ParentContract {
    modifier firstModifier() {
        _;
    }
    
    modifier secondModifier() {
        _;
    }

    function withNoModifiers() public { }

    function withParentModifier() public parentModifier { }    

    function withOneModifier() internal firstModifier { }
    
    function withTwoModifiers(address) public firstModifier secondModifier { }
}
