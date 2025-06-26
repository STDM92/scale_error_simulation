from dataclasses import dataclass


@dataclass(frozen=True)
class PopulationConfig():
    population_size: float


default = PopulationConfig(population_size=1_000)
small = PopulationConfig(population_size=100)
medium = PopulationConfig(population_size=10_000)
large = PopulationConfig(population_size=1_000_000)