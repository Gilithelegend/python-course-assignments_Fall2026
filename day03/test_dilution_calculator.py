import unittest

from dilution_calculator import calculate_dilution
from dilution_examples import EXAMPLE_CASES


class TestCalculateDilution(unittest.TestCase):
    def test_generated_cases(self):
        for case in EXAMPLE_CASES:
            with self.subTest(case=case["name"]):
                result = calculate_dilution(**case["inputs"])
                self.assertAlmostEqual(
                    result[0], case["expected"]["stock_volume"]
                )
                self.assertAlmostEqual(
                    result[1], case["expected"]["water_volume"]
                )

    def test_rejects_target_concentration_above_stock(self):
        with self.assertRaises(ValueError):
            calculate_dilution(1, "M", 2, "M", 10, "mL")


if __name__ == "__main__":
    unittest.main()
