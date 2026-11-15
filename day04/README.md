# Day 04 - Dilution Calculator as a Flask web app

I copied my day03 dilution calculator into this folder and added a web
interface with Flask. The calculation itself is unchanged: `dilution_web.py`
imports `calculate_dilution()` from `dilution_calculator.py`.

## How to run

    python3 -m pip install flask
    python3 dilution_web.py

Then open http://127.0.0.1:5002 and press Ctrl+C in the terminal to stop.

Example: stock 1 M, target 100 mM, final volume 50 mL gives
"Mix 5 mL of stock with 45 mL of water."

## Check the old version still works

    python3 -m unittest
    python3 dilution_calculator_ui.py

## What I did

- Copied day03 to day04 with `cp -r day03 day04`.
- Wrote `dilution_web.py`: a form with three numbers and three unit dropdowns.
  On submit, Flask reads the values with `request.form`, converts the numbers
  with `float()`, calls `calculate_dilution()` and shows the result.
- Bad input (an empty box, or a target above the stock) shows an error
  message instead of crashing.
- Added `__pycache__/` to `.gitignore`.

## Files

| File | What it does |
| --- | --- |
| `dilution_web.py` | New: the Flask web app |
| `dilution_calculator.py` | The calculation, copied from day03 |
| `dilution_calculator_ui.py` | The old day03 browser UI |
| `dilution_test_cases.json`, `dilution_examples.py`, `test_dilution_calculator.py` | The day03 test data and tests |

## AI used: Claude

I work in a Claude Project I set up for this course. I gave it the course
README and the day notes, and instructions to teach me instead of handing me
the solution: explain the idea, show a small example, give hints first, and
give the full answer only when I am stuck. What I asked for in this
assignment:

1. I pasted the Day 4 notes and the assignment text and asked what I need to
   do and how Flask works.
2. I asked for a small practice example of a Flask form before the real app
   (a page that doubles a number), and ran it myself.
3. I asked how to turn my day03 `calculate_dilution()` function into a web
   page. Claude gave me the HTML form and hints, and then the final `home()`
   function, with an explanation of every line.
4. I pasted my terminal errors (copying the folder from the wrong place,
   "Port 5001 is in use", a wrong file name, a paste that created a
   SyntaxError) and asked what each one means and how to fix it.
