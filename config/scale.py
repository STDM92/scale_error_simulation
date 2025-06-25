from dataclasses import dataclass

@dataclass(frozen=True)
class ScaleConfig:
    scale_error:       float
    scale_error_unit:  str
    scale_resolution:  float
    resolution_unit:   str

# presets
cube_scale = ScaleConfig(
    scale_error=0.00016 * 50000,
    scale_error_unit="g",
    scale_resolution=0.01,
    resolution_unit="g",
)

aec_scale = ScaleConfig(
    scale_error=0.00016 * 50000,
    scale_error_unit="g",
    scale_resolution=1.0,
    resolution_unit="g",
)

abc_scale = ScaleConfig(
    scale_error=0.00016 * 50000,
    scale_error_unit="g",
    scale_resolution=1.0,
    resolution_unit="g",
)
