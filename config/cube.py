from dataclasses import dataclass

@dataclass(frozen=True)
class CubeConfig:
    base_weight:      float
    base_weight_unit: str
    part_tolerance:   float
    tolerance_unit:   str


default = CubeConfig(
    base_weight=2500.0,
    base_weight_unit="g",
    part_tolerance=5.0,
    tolerance_unit="g",
)


light = CubeConfig(
    base_weight=250.0,
    base_weight_unit="g",
    part_tolerance=1.0,
    tolerance_unit="g",
)

heavy = CubeConfig(
    base_weight=25000.0,
    base_weight_unit="g",
    part_tolerance=5.0,
    tolerance_unit="g",
)
