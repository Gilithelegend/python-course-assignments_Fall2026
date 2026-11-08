import math


_CONCENTRATION_TO_MOLAR = {
    "M": 1.0,
    "mM": 1e-3,
    "µM": 1e-6,
    "uM": 1e-6,
    "nM": 1e-9,
}

_VOLUME_TO_LITERS = {
    "L": 1.0,
    "mL": 1e-3,
    "µL": 1e-6,
    "uL": 1e-6,
}


def calculate_dilution(
    stock_concentration: float,
    stock_unit: str,
    target_concentration: float,
    target_unit: str,
    final_volume: float,
    volume_unit: str,
) -> tuple[float, float]:
    """Return (stock volume, water volume) in the final volume's unit."""
    stock_factor = _CONCENTRATION_TO_MOLAR.get(stock_unit.replace("μ", "µ"))
    target_factor = _CONCENTRATION_TO_MOLAR.get(target_unit.replace("μ", "µ"))
    volume_factor = _VOLUME_TO_LITERS.get(volume_unit.replace("μ", "µ"))
    if stock_factor is None:
        raise ValueError(f"Unsupported stock concentration unit: {stock_unit}")
    if target_factor is None:
        raise ValueError(f"Unsupported target concentration unit: {target_unit}")
    if volume_factor is None:
        raise ValueError(f"Unsupported volume unit: {volume_unit}")

    values = (stock_concentration, target_concentration, final_volume)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Concentrations and volume must be finite numbers")
    if stock_concentration <= 0:
        raise ValueError("Stock concentration must be greater than zero")
    if target_concentration < 0:
        raise ValueError("Target concentration cannot be negative")
    if final_volume <= 0:
        raise ValueError("Final volume must be greater than zero")

    stock_molar = stock_concentration * stock_factor
    target_molar = target_concentration * target_factor
    if target_molar > stock_molar:
        raise ValueError("Target concentration cannot exceed stock concentration")

    final_volume_liters = final_volume * volume_factor
    stock_volume_liters = target_molar * final_volume_liters / stock_molar
    stock_volume = stock_volume_liters / volume_factor
    water_volume = final_volume - stock_volume
    return stock_volume, water_volume
