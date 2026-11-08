import html
import math
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from dilution_calculator import calculate_dilution
from dilution_examples import EXAMPLE_CASES


HOST = "127.0.0.1"
PORT = 8000
CONCENTRATION_UNITS = ("M", "mM", "µM", "nM")
VOLUME_UNITS = ("L", "mL", "µL")


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _unit_options(units: tuple[str, ...], selected: str) -> str:
    return "".join(
        f'<option value="{_escape(unit)}"'
        f'{" selected" if unit == selected else ""}>'
        f"{_escape(unit)}</option>"
        for unit in units
    )


def _page(
    *,
    stock: str = "1",
    stock_unit: str = "M",
    target: str = "100",
    target_unit: str = "mM",
    final_volume: str = "50",
    volume_unit: str = "mL",
    result: str = "",
    error: str = "",
) -> str:
    message = ""
    if error:
        message = f'<p class="error">{_escape(error)}</p>'
    elif result:
        message = f'<p class="result">{_escape(result)}</p>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dilution Calculator</title>
  <style>
    body {{ margin: 2rem auto; padding: 0 1rem; max-width: 650px;
      font: 16px Arial, sans-serif; color: #202124; }}
    h1 {{ margin-bottom: .4rem; }}
    p {{ line-height: 1.5; }}
    form {{ display: grid; grid-template-columns: 1fr 150px 90px;
      gap: 12px; align-items: center; margin: 1.5rem 0; }}
    input, select, button {{ box-sizing: border-box; min-height: 42px;
      padding: 8px; font-size: 16px; }}
    input {{ width: 100%; border: 1px solid #666; border-radius: 4px; }}
    button {{ grid-column: 1 / -1; cursor: pointer; }}
    .result {{ padding: 12px; background: #e8f5e9; border-radius: 4px; }}
    .error {{ padding: 12px; color: #8b0000; background: #ffebee;
      border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
    @media (max-width: 480px) {{
      form {{ grid-template-columns: 1fr 100px 75px; gap: 8px; }}
    }}
  </style>
</head>
<body>
  <h1>Dilution Calculator</h1>
  <p>Enter your stock concentration, target concentration, and final volume.</p>
  {message}
  <form method="post" action="/calculate">
    <label for="stock">Stock concentration</label>
    <input id="stock" name="stock" type="number" step="any"
      value="{_escape(stock)}" required>
    <select name="stock_unit" aria-label="Stock concentration unit">
      {_unit_options(CONCENTRATION_UNITS, stock_unit)}
    </select>

    <label for="target">Target concentration</label>
    <input id="target" name="target" type="number" step="any"
      value="{_escape(target)}" required>
    <select name="target_unit" aria-label="Target concentration unit">
      {_unit_options(CONCENTRATION_UNITS, target_unit)}
    </select>

    <label for="final_volume">Final volume</label>
    <input id="final_volume" name="final_volume" type="number" step="any"
      value="{_escape(final_volume)}" required>
    <select name="volume_unit" aria-label="Final volume unit">
      {_unit_options(VOLUME_UNITS, volume_unit)}
    </select>

    <button type="submit">Calculate</button>
  </form>
  <p><a href="/tests">View tested data and results</a></p>
</body>
</html>"""


def _tests_page() -> str:
    rows = []
    for case in EXAMPLE_CASES:
        name = case["name"]
        inputs = case["inputs"]
        expected = case["expected"]
        stock = inputs["stock_concentration"]
        stock_unit = inputs["stock_unit"]
        target = inputs["target_concentration"]
        target_unit = inputs["target_unit"]
        final = inputs["final_volume"]
        volume_unit = inputs["volume_unit"]
        actual = calculate_dilution(**inputs)
        passed = all(
            math.isclose(value, expected_value, rel_tol=1e-9, abs_tol=1e-9)
            for value, expected_value in zip(
                actual,
                (expected["stock_volume"], expected["water_volume"]),
            )
        )
        rows.append(
            "<tr>"
            f"<td>{_escape(name)}</td>"
            f"<td>Stock {stock} {_escape(stock_unit)}; "
            f"target {target} {_escape(target_unit)}; "
            f"final {final} {_escape(volume_unit)}</td>"
            f"<td>{expected['stock_volume']} + "
            f"{expected['water_volume']} {_escape(volume_unit)}</td>"
            f"<td>{actual[0]:.6g} + {actual[1]:.6g} "
            f"{_escape(volume_unit)}</td>"
            f"<td>{'PASS' if passed else 'FAIL'}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tested examples - Dilution Calculator</title>
  <style>
    body {{ margin: 2rem auto; padding: 0 1rem; max-width: 950px;
      font: 16px Arial, sans-serif; color: #202124; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
  </style>
</head>
<body>
  <h1>Test data and results</h1>
  <table>
    <thead><tr><th>Case</th><th>Input</th><th>Expected stock + water</th>
      <th>Actual stock + water</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
  <p><a href="/">Back to calculator</a></p>
</body>
</html>"""


class DilutionRequestHandler(BaseHTTPRequestHandler):
    def _send_html(self, content: str, status: int = 200) -> None:
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_html(_page())
        elif self.path == "/tests":
            self._send_html(_tests_page())
        else:
            self._send_html("<h1>Not found</h1>", status=404)

    def do_POST(self) -> None:
        if self.path != "/calculate":
            self._send_html("<h1>Not found</h1>", status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 10_000:
                raise ValueError("Form submission is too large")
            form = parse_qs(
                self.rfile.read(length).decode("utf-8"),
                strict_parsing=True,
            )

            def value(name: str) -> str:
                return form[name][0]

            fields = {
                "stock": value("stock"),
                "stock_unit": value("stock_unit"),
                "target": value("target"),
                "target_unit": value("target_unit"),
                "final_volume": value("final_volume"),
                "volume_unit": value("volume_unit"),
            }
            if fields["stock_unit"] not in CONCENTRATION_UNITS:
                raise ValueError("Select a supported stock concentration unit")
            if fields["target_unit"] not in CONCENTRATION_UNITS:
                raise ValueError("Select a supported target concentration unit")
            if fields["volume_unit"] not in VOLUME_UNITS:
                raise ValueError("Select a supported volume unit")

            stock_volume, water_volume = calculate_dilution(
                float(fields["stock"]),
                fields["stock_unit"],
                float(fields["target"]),
                fields["target_unit"],
                float(fields["final_volume"]),
                fields["volume_unit"],
            )
        except (KeyError, IndexError, UnicodeDecodeError, ValueError) as error:
            values = locals().get("fields", {})
            defaults = {
                "stock": "1",
                "stock_unit": "M",
                "target": "100",
                "target_unit": "mM",
                "final_volume": "50",
                "volume_unit": "mL",
            }
            defaults.update(values)
            self._send_html(_page(**defaults, error=str(error)), status=400)
            return

        self._send_html(
            _page(
                **fields,
                result=(
                    f"Add {stock_volume:.6g} {fields['volume_unit']} stock "
                    f"+ {water_volume:.6g} {fields['volume_unit']} water."
                ),
            )
        )

    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DilutionRequestHandler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Dilution Calculator is running at {url}")
    print("Press Ctrl+C to stop the server.")
    threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dilution Calculator.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
