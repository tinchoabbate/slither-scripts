#!/usr/bin/python3
import sys
from slither.slither import Slither
from constants import ERC20_EVENT_SIGNATURES, ERC20_FX_SIGNATURES, ERC20_GETTERS


def is_visible(function):
    return is_public(function) or is_external(function)


def is_external(e):
    return e.visibility == "external"


def is_public(e):
    return e.visibility == "public"


def find_match(elements, signature):
    """
    Returns True if at least one element's signature
    matches the expected signature
    """
    return any(e.signature == signature for e in elements)


def verify_signatures(elements, expected_signatures):
    """
    Compares a list of elements and expected signatures.
    Returns a list containing the results of the comparison.
    """
    return [(sig, find_match(elements, sig)) for sig in expected_signatures]


def get_return_type(signature):
    """Returns the first return type of a signature"""
    return signature[2][0]


def name_and_return_match(variable, signature):
    return (variable.name == signature[0] and
            str(variable.type) == get_return_type(signature))


def verify_getters(state_variables, functions, expected_getters):
    getters = []
    for getter in expected_getters:
        # Check in state variables. If none is found, check in functions.
        if (
            any(name_and_return_match(v, getter) and is_public(v) for v in state_variables) or
            find_match(functions, getter)
        ):
            getters.append((getter, True))
        else:
            getters.append((getter, False))

    return getters


def get_visible_functions(functions):
    """Filters a list of functions, keeping the visible ones"""
    return [f for f in functions if is_visible(f)]


def signature_to_string(signature):
    result = f"{signature[0]} ({', '.join(signature[1])})"
    if len(signature) == 3:
        result = f"{result} -> ({', '.join(signature[2])})"
    return result


def log_matches(matches):
    for match in matches:
        marker = '\u2713' if match[1] else 'x'
        print(f"[{marker}] {signature_to_string(match[0])}")


def run(filename, contract_name):
    # Init Slither
    slither = Slither(filename)

    # Get an instance of the contract to be analyzed
    contract = slither.get_contract_from_name(contract_name)
    if not contract:
        print(f"Contract {contract_name} not found")
        exit(-1)

    # Obtain visible functions
    visible_functions = get_visible_functions(contract.functions)

    # Check signature matches for functions and events
    function_matches = verify_signatures(visible_functions, ERC20_FX_SIGNATURES)
    event_matches = verify_signatures(contract.events, ERC20_EVENT_SIGNATURES)

    print("== ERC20 functions ==")
    log_matches(function_matches)
    
    print("\n== ERC20 events ==")
    log_matches(event_matches)

    getters_matches = verify_getters(
        contract.state_variables,
        visible_functions,
        ERC20_GETTERS
    )
    print("\n== ERC20 getters ==")
    log_matches(getters_matches)
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python erc20.py <contract.sol> <contract-name>')
        exit(-1)
    
    filename = sys.argv[1]
    contract_name = sys.argv[2]
    run(filename, contract_name)
