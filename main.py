#!/usr/bin/env python3
from math import ceil

# -------------------------------------------------
# Recipes: customize this with your game data
# -------------------------------------------------
# output_per_s and input rates are "items per second"
recipes = {
    "Fertilizer": {
        "machine": "Assembler",
        "output_per_s": 0.25,        # 0.25 Fertilizer per second
        "time_s": 4,
        "inputs": {
            "Plant Ask": 0.25,
            "Quicklime Powder": 0.25
        }
    },
    "Plant Ask": {
        "machine": "Crucible",
        "output_per_s": 0.333333333,
        "time_s": 3,
        "inputs": {
            "Sage": 0.333333333
        }
    },
    "Quicklime Powder": {
        "machine": "Grinder",
        "output_per_s": 0.111666667,
        "time_s": 9,
        "inputs": {
            "Quicklime": 0.111666667
        }
    },
    "Quicklime": {
        "machine": "Crucible",
        "output_per_s": 0.111666667,
        "time_s": 9,
        "inputs": {
            "Stone": 0.111666667
        }
    },
    "Stone": {
        "machine": "Stone Crusher",
        "output_per_s": 30/60,
        "time_s": 2,
        "inputs": {
            "Logs": 0.15/60
        }
    },
    "Plank": {
        "machine": "Table Saw",
        "output_per_s": 30/60,
        "time_s": 2,
        "inputs": {
            "Logs": 0.15/60
        }
    },
    "Sand": {
        "machine": "Grinder",
        "output_per_s": 5/60,
        "time_s": 12,
        "inputs": {
            "Stone": 5/60
        }
    },
    "Glass": {
        "machine": "Kiln",
        "output_per_s": 10/60,
        "time_s": 6,
        "inputs": {
            "Sand": 60/60
        }
    }
}

# -------------------------------------------------
# Core calculation logic
# -------------------------------------------------
def calc_requirements(target_item, target_qty_per_min, machines=None, base_inputs=None):
    """
    Recursively calculate machines and base inputs
    needed to produce target_qty_per_min of target_item.
    Returns: (machines_dict, base_inputs_dict)
    """
    if machines is None:
        machines = {}
    if base_inputs is None:
        base_inputs = {}

    # If there is no recipe, it is a base resource
    if target_item not in recipes:
        base_inputs[target_item] = base_inputs.get(target_item, 0) + target_qty_per_min
        return machines, base_inputs

    recipe = recipes[target_item]

    out_per_min = recipe["output_per_s"] * 60.0
    if out_per_min <= 0:
        raise ValueError(f"Invalid output_per_s for item: {target_item}")

    machines_needed = target_qty_per_min / out_per_min
    machine_name = recipe["machine"]
    machines[machine_name] = machines.get(machine_name, 0) + machines_needed

    # For each input, compute required quantity per minute and recurse
    for input_item, input_rate_per_s in recipe["inputs"].items():
        ratio = input_rate_per_s / recipe["output_per_s"]  # input per 1 output
        required_per_min = ratio * target_qty_per_min
        calc_requirements(input_item, required_per_min, machines, base_inputs)

    return machines, base_inputs


def parse_number(text: str) -> float:
    """
    Accept both "60" and "60,5" formats.
    """
    text = text.strip().replace(",", ".")
    return float(text)


# -------------------------------------------------
# Terminal UI
# -------------------------------------------------
def print_header():
    print("=" * 50)
    print("        ALCHEMY FACTORY RATIO CALCULATOR")
    print("=" * 50)


def list_items():
    print("\nAvailable craftable items:")
    for i, name in enumerate(sorted(recipes.keys()), start=1):
        r = recipes[name]
        per_min = r["output_per_s"] * 60
        print(f"  {i:2d}. {name:15s} -> {per_min:.3f}/min ({r['machine']})")
    print()


def show_recipe(item_name):
    r = recipes[item_name]
    print(f"\nRecipe for {item_name}:")
    print(f"  Machine: {r['machine']}")
    print(f"  Cycle time: {r['time_s']} s")
    print(f"  Output: {r['output_per_s']} per second ({r['output_per_s']*60:.3f} per minute)")
    print("  Inputs:")
    for inp, rate in r["inputs"].items():
        ratio = rate / r["output_per_s"]
        print(f"    - {inp}: {ratio:.4f} per 1 {item_name}")
    print()


def run_calculation():
    list_items()
    item = input("Target item name (exact, e.g. Fertilizer): ").strip()
    if item not in recipes:
        print(f"Item '{item}' not found in recipes.\n")
        return

    qty_str = input("Desired quantity per minute (e.g. 60): ").strip()
    try:
        qty = parse_number(qty_str)
    except ValueError:
        print("Invalid number.\n")
        return
    if qty <= 0:
        print("Quantity must be greater than 0.\n")
        return

    machines, base_inputs = calc_requirements(item, qty)

    print("\n" + "-" * 50)
    print(f"Target: {qty:.4g} {item} / minute")
    print("-" * 50)

    # Machines
    print("\nMachines needed:")
    if not machines:
        print("  (none)")
    else:
        for m, val in sorted(machines.items()):
            print(f"  - {m:15s} : {ceil(val):4d} (exact: {val:.4f})")

    # Base inputs
    print("\nBase inputs per minute (items without recipes):")
    if not base_inputs:
        print("  (none)")
    else:
        for res, val in sorted(base_inputs.items()):
            print(f"  - {res:15s} : {val:.4f} / min")

    print()


def main_menu():
    while True:
        print_header()
        print("1) List items")
        print("2) Show recipe for an item")
        print("3) Calculate machine ratios")
        print("4) Quit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_items()
            input("Press Enter to continue...")
        elif choice == "2":
            list_items()
            name = input("Item name to inspect: ").strip()
            if name in recipes:
                show_recipe(name)
            else:
                print("Item not found.\n")
            input("Press Enter to continue...")
        elif choice == "3":
            run_calculation()
            input("Press Enter to continue...")
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main_menu()
