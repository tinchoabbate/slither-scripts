#!/usr/bin/python3
import sys
from slither.slither import Slither
from slither.slithir.operations.event_call import EventCall
from constants import ERC20_EVENT_SIGNATURES, ERC20_FX_SIGNATURES, ERC20_GETTERS, ERC20_EVENT_BY_FUNCTION


def is_visible(function):
    """Returns True if function is public or external"""
    return is_public(function) or is_external(function)


def is_external(f):
    """Returns True if function's visibility is external"""
    return f.visibility == "external"


def is_public(e):
    """Returns True if the element's visibility is public"""
    return e.visibility == "public"


def dict_to_tuple(dic):
    """Returns a tuple containing the values of the given dict"""
    return tuple(dic.values())


def find_match(elements, signature):
    """
    Returns the element (Function or Event) that matches the given signature.
    None otherwise.
    """
    return next((e for e in elements if e.signature == dict_to_tuple(signature)), None)


def verify_signatures(elements, expected_signatures):
    """
    Compares a list of elements (functions or events) and expected signatures.
    Returns a list of tuples containing the results of the comparison such as:
    (signature dict, matching object)
    """
    return [(sig, find_match(elements, sig)) for sig in expected_signatures]


def name_and_return_match(variable, signature):
    return (variable.name == signature["name"] and
            str(variable.type) == signature["returns"][0])


def verify_getters(state_variables, functions, expected_getters):
    for getter in expected_getters:
        # Check in state variables. If none is found, check in functions.
        if (
            any(name_and_return_match(v, getter) and is_public(v) for v in state_variables) or
            find_match(functions, getter)
        ):
            yield (getter, True)
        else:
            yield (getter, False)


def get_visible_functions(functions):
    """Filters a list of functions, keeping the visible ones"""
    return [f for f in functions if is_visible(f)]


def signature_to_string(signature, print_return=True):
    result = f"{signature['name']} ({', '.join(signature['args'])})"    
    if len(signature) == 3 and print_return:
        result = f"{result} -> ({', '.join(signature['returns'])})"    
    return result


def log_matches(matches, print_events=False):
    for match in matches:
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {signature_to_string(match[0])}")


def log_event_per_function(matches):
    for match in matches:
        function_name = match[0]["name"]
        expected_event = signature_to_string(ERC20_EVENT_BY_FUNCTION[function_name])
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {function_name} must emit {expected_event}")


def is_event_call(ir):
    return isinstance(ir, EventCall)


def get_events(function):
    """Returns a generator to iterate over the events emitted by the function"""
    for node in getattr(function, 'nodes', []):
        for ir in node.irs:
            if is_event_call(ir):
                yield ir


def emits_event(function, expected_event):
    """Returns True if the function (or internal calls) emits the given event. False otherwise."""
    for event in get_events(function):
        if (
            event.name == expected_event["name"] and 
            all(str(arg.type) == expected_event["args"][i] for i, arg in enumerate(event.arguments))
        ):
            return True
    
    # Event is not fired in function, so check internal calls to other functions
    if any(emits_event(f, expected_event) for f in getattr(function, 'internal_calls', [])):
        return True

    # Event is not fired in function nor in internal calls
    return False


def verify_erc20_event_calls(function_matches):
    """Returns a generator"""
    for match in function_matches:
        if match[1] and ERC20_EVENT_BY_FUNCTION[match[0]["name"]]:
            yield (match[0], emits_event(match[1], ERC20_EVENT_BY_FUNCTION[match[1].name]))


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
    event_definition_matches = verify_signatures(contract.events, ERC20_EVENT_SIGNATURES)
    
    functions_firing_events = verify_erc20_event_calls(function_matches)

    print("== ERC20 functions ==")
    log_matches(function_matches)
    
    print("\n== ERC20 events ==")
    log_matches(event_definition_matches)

    log_event_per_function(functions_firing_events)

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
