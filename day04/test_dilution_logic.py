import pytest

from dilution_calculator import calculate_dilution


def test_simple_dilution():
    # 1 M stock to 100 mM in 50 mL: C1*V1 = C2*V2 gives 5 mL stock + 45 mL water
    stock_volume, water_volume = calculate_dilution(1, "M", 100, "mM", 50, "mL")
    assert stock_volume == pytest.approx(5)
    assert water_volume == pytest.approx(45)


def test_small_units():
    # 2 mM stock to 500 µM in 200 µL: a 4x dilution, so 50 µL stock + 150 µL water
    stock_volume, water_volume = calculate_dilution(2, "mM", 500, "µM", 200, "µL")
    assert stock_volume == pytest.approx(50)
    assert water_volume == pytest.approx(150)


def test_volumes_add_up_to_final_volume():
    stock_volume, water_volume = calculate_dilution(10, "mM", 3, "mM", 25, "mL")
    assert stock_volume + water_volume == pytest.approx(25)


def test_target_equal_to_stock_needs_no_water():
    stock_volume, water_volume = calculate_dilution(5, "mM", 5, "mM", 10, "mL")
    assert stock_volume == pytest.approx(10)
    assert water_volume == pytest.approx(0)


def test_target_above_stock_is_an_error():
    with pytest.raises(ValueError):
        calculate_dilution(1, "mM", 1, "M", 10, "mL")


def test_unknown_unit_is_an_error():
    with pytest.raises(ValueError):
        calculate_dilution(1, "M", 100, "mM", 50, "gallons")