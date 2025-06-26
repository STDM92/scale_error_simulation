import config as cfg
from utils.console_style import BOLD, RED, CYAN, RESET_ALL
import numpy as np
import pandas as pd


class Population:
    def __init__(

            self,
            cube_cfg: cfg.cube,
            pop_cfg: cfg.population,
            scale_cfg: cfg.scale,
            seed: int | None = None
    ) -> None:
        self._rng = np.random.default_rng(seed)
        if seed is not None: np.random.seed(seed)
        self.cube = cube_cfg
        self.n = pop_cfg.population_size
        self.scale = scale_cfg
        self.df : pd.DataFrame | None = None


    def simulate(self) -> pd.DataFrame:
        """
        --- Generate Dataframe with all populations stats ---

                Simulate true cube weights of population N based on part tolerances
                Simulate measured cube weights based on real weights + random scale error
                Calculate measurement error
        """
        true_weight = self.cube.base_weight+ self._rng.normal(
            loc=0,
            scale=self.cube.part_tolerance,
            size=self.n
        )

        measured_weight = true_weight + self._rng.normal(
            loc=0,
            scale=self.scale.scale_error,
            size=self.n
        )

        self.df = pd.DataFrame({
            "true_weight": true_weight,
            "measured": measured_weight,
            "measurement_err": measured_weight - true_weight,
        })

        return self.df



    def print_cube(self):
        print(f"{BOLD}The current cube configuration is as following:{RESET_ALL}")
        print(f"{RED}Base Weight:{RESET_ALL} {self.cube.base_weight}{self.cube.base_weight_unit}")
        print(f"{CYAN}Part Tolerance:{RESET_ALL} {self.cube.part_tolerance}{self.cube.tolerance_unit}")


    def summary(self) -> dict:
        df = self.df() if self.df is not None else self.simulate()
        print(df.describe())
        return {
            "mean_err": df.measurement_err.mean(),
            "std_err": df.measurement_err.std(),
        }

    def plot_errors(self, ax=None):
        import matplotlib.pyplot as plt
        df = self.df if self.df is not None else self.simulate()
        ax = ax or plt.gca()
        ax.hist(df.measurement_err, bins='auto')
        ax.set(title="Error Distribution", xlabel="Error", ylabel="Count")
        return ax

    def plot_measured_weights(self, ax=None):
        import matplotlib.pyplot as plt
        df = self.df if self.df is not None else self.simulate()
        ax = ax or plt.gca()
        ax.hist(df.measured, bins='auto')
        ax.set(title="Measured Weights", xlabel="Weight", ylabel="Count")
        return ax

    def plot_true_weights(self, ax=None):
        import matplotlib.pyplot as plt
        df = self.df if self.df is not None else self.simulate()
        ax = ax or plt.gca()
        ax.hist(df.true_weight, bins='auto')
        ax.set(title="True Weights", xlabel="Weight", ylabel="Count")
        return ax
