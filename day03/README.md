# Dilution Calculator

This folder contains a Python dilution calculator that uses `C1V1 = C2V2` to
calculate the stock volume and water volume needed to make a target solution.

## Run the browser UI

Open a terminal in this `day03` folder and run:

```bash
python3 dilution_calculator_ui.py
```

The calculator opens in your browser at <http://127.0.0.1:8000/>. Keep the
terminal open while using it; press `Ctrl+C` in the terminal to stop it.

Enter the stock concentration, target concentration, and final volume in the
form. Choose a unit for each value and click **Calculate**. The result gives
the volume of stock and water to mix. The **View tested data and results** link
shows the saved example cases, their expected and calculated results, and
whether each one passes.

## Use the function from Python

Import `calculate_dilution` from `dilution_calculator.py`. It returns a pair:
`(stock_volume, water_volume)`, using the same volume unit as the final volume.

```python
from dilution_calculator import calculate_dilution

stock_volume, water_volume = calculate_dilution(
    1, "M",       # stock concentration and unit
    100, "mM",    # target concentration and unit
    50, "mL",     # final volume and unit
)

print(stock_volume, water_volume)  # 5.0 45.0
```

Supported concentration units: `M`, `mM`, `µM`, and `nM` (also accepts `uM`).
Supported volume units: `L`, `mL`, and `µL` (also accepts `uL`).

## Test

Run the unit tests from this folder:

```bash
python3 -m unittest -v
```

The example inputs and expected stock/water volumes are stored in
[`dilution_test_cases.json`](dilution_test_cases.json). The unit tests and the
browser's tested-results page both use this file.

## What I did

I built a small Python program that does a common lab computation: a dilution
calculation (`C1·V1 = C2·V2`). Given a stock concentration, a target
concentration, and a target volume, the `calculate_dilution()` function returns
how much stock and how much water (diluent) to mix.

Files in this folder:

| File | What it does |
| --- | --- |
| `dilution_calculator.py` | The computation: `calculate_dilution()` |
| `dilution_calculator_ui.py` | A simple browser UI that runs the calculator and shows test data and results (PASS / FAIL) |
| `dilution_test_cases.json` | Hand-written test cases with inputs and expected stock/water volumes |
| `dilution_examples.py` | Loads the test cases from the JSON file |
| `test_dilution_calculator.py` | Unit tests that run every JSON case against `calculate_dilution()` |

The test cases are written manually, not randomly. Each case has input values
and an expected result. Both the UI and the unit tests read the same JSON file,
so editing it updates both.

## Tools used

- GitHub Copilot (AI chat) in VS Code
- Git plugin in VS Code for commits and pushing to the assignment repository

## Prompts I wrote to Copilot

Below are prompts from my Copilot chat and a summary of what Copilot did with
each.

1. "Are the test cases random? Where are they stored?" — Asked how the test
   data works. Copilot explained that the cases are written manually and that
   the UI runs them through `calculate_dilution()` and shows PASS / FAIL.
2. "put the test cases in a file" — Copilot moved the cases into
   `dilution_test_cases.json` and updated `dilution_examples.py`,
   `dilution_calculator_ui.py`, and `test_dilution_calculator.py` to read from
   it. It then ran the tests, which passed.
3. "i need it in a file" — Copilot confirmed that
   `day03/dilution_test_cases.json` exists and can be opened and edited in VS
   Code.

## How to run

Run the browser UI from this folder:

```bash
python dilution_calculator_ui.py
```

Run the tests with pytest:

```bash
python -m pytest test_dilution_calculator.py
```
