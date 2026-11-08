import json
from pathlib import Path


with Path(__file__).with_name("dilution_test_cases.json").open(
    encoding="utf-8"
) as test_cases_file:
    EXAMPLE_CASES = json.load(test_cases_file)
