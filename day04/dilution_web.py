from flask import Flask, request
from dilution_calculator import calculate_dilution   # your day03 function

app = Flask(__name__)

PAGE = """
<h1>Dilution Calculator</h1>
<form method="post">
  Stock concentration: <input name="stock">
  <select name="stock_unit"><option>M</option><option>mM</option><option>µM</option><option>nM</option></select><br><br>
  Target concentration: <input name="target">
  <select name="target_unit"><option>M</option><option>mM</option><option>µM</option><option>nM</option></select><br><br>
  Final volume: <input name="volume">
  <select name="volume_unit"><option>L</option><option>mL</option><option>µL</option></select><br><br>
  <button>Calculate</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":                      # the user clicked Calculate
        try:
            unit = request.form["volume_unit"]        # e.g. "mL"
            stock_volume, water_volume = calculate_dilution(
                float(request.form["stock"]),         # numbers arrive as text, so float()
                request.form["stock_unit"],           # units stay text
                float(request.form["target"]),
                request.form["target_unit"],
                float(request.form["volume"]),
                unit,
            )
            return PAGE + f"Mix {stock_volume:g} {unit} of stock with {water_volume:g} {unit} of water."
        except ValueError as problem:                 # bad input, e.g. empty box or target > stock
            return PAGE + f"Error: {problem}"
    return PAGE                                       # first visit: just the form

app.run(debug=True, port=5002)