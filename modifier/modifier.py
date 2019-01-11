from slither import Slither
from slither.utils.colors import blue, green, magenta, yellow
import collections
import sys


def filter_by_modifier(functions, modifier_name):
    for f in functions:
        if modifier_name in [m.name for m in f.modifiers]:
            yield f


def run(filename, mod_name):
    """Executes script"""

    # Init Slither
    slither = Slither(filename)
    if not len(slither.contracts):
        print(f"Error: Slither could not find any contracts")
        exit(-1)

    print(f"== Functions with {yellow(mod_name)} modifier ==")
    txt = ""
    for c in slither.contracts:
            txt += blue(f"\n+ Contract {c.name}\n")

            collect = collections.defaultdict(list)

            for f in filter_by_modifier(c.functions, mod_name):
                collect[f.contract.name].append((f.full_name, f.visibility))
            
            for contract, function_visi_pairs in collect.items():
                txt += blue(f"  - From {contract}\n")
                
                function_visi_pairs = sorted(function_visi_pairs)

                for function, visi in function_visi_pairs:
                    if visi in ['external', 'public']:
                        txt += green(f"    - {function} ({visi})\n")
                
                for function, visi in function_visi_pairs:
                    if visi in ['internal', 'private']:
                        txt += magenta(f"    - {function} ({visi})\n")
                
                for function, visi in function_visi_pairs:
                    if visi not in ['external', 'public', 'internal', 'private']:
                        txt += f"    - {function}  ({visi})\n"

    print(txt)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python modifier.py <contract.sol> <modifier-name>')
        exit(-1)

    FILE_NAME = sys.argv[1]
    mod_name = sys.argv[2]
    run(FILE_NAME, mod_name)
