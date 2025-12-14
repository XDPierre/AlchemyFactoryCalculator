# Alchemy Factory – Terminal Production Ratio Calculator

A lightweight terminal-based tool that calculates machine requirements and resource consumption for items in **Alchemy Factory**. Given a target item and a desired production rate per minute, the calculator recursively evaluates all required recipes and outputs the number of machines and base materials needed for stable production.

This tool removes guesswork from factory planning and provides accurate throughput information.

---

## Features

### Recursive Production Solver
- Automatically processes all crafting dependencies.
- Computes per-minute input and output requirements.
- Calculates exact and rounded-up machine counts.
- Supports multi-level production chains.

### Terminal-Based Interface
- Simple text-only interaction.
- Menu options for viewing items, inspecting recipes, and running calculations.
- Works on Windows, macOS, and Linux.

### Easy Recipe Customization
- Recipes are stored in a Python dictionary.
- Users can freely edit or add items.
- Supports modded or custom versions of *Alchemy Factory*.

---

## How It Works

1. Select a target item (for example: `Fertilizer`).
2. Enter the desired production rate per minute (for example: `60`).
3. The calculator determines:
   - Number of machines required at every stage.
   - Production ratios for all intermediate items.
   - Base resources needed per minute.

The system uses output-per-second values and input ratios to compute everything recursively.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/XDPierre/AlchemyFactoryCalculator.git
cd ./AlchemyFactoryCalculator
```

Run the program:

```bash
python main.py
```

Python 3.8 or newer is required.

---

## Usage

When running the script, a menu appears:

```
1) List items
2) Show recipe for an item
3) Calculate machine ratios
4) Quit
```

Choose option 3 to calculate machine requirements.

Example output:

```
Target: 60 Fertilizer / minute

Machines needed:
- Assembler     : 4 (exact: 4.0000)
- Crucible      : 12 (exact: 12.0000)
- Grinder       : 9 (exact: 9.0000)
- Stone Crusher : 3 (exact: 3.0000)

Base inputs per minute:
- Sage      : 60.0000
- Limestone : 60.0000
```

---

## Customizing Recipes

Edit the `recipes` dictionary inside the script:

```python
recipes = {
    "Fertilizer": {
        "machine": "Assembler",
        "output_per_s": 0.25,
        "inputs": {
            "Plant Ask": 0.25,
            "Quicklime Powder": 0.25
        }
    }
}
```

The calculator automatically resolves any added items.

---

## Roadmap

Planned improvements:

- CSV or JSON recipe importing
- Validation tools for recipe structures
- Graph visualization for production trees
- Optional web-based interface

---

## License

Released under the MIT License.
