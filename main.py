import config as cfg
from simulation.population import Population
import utils.GUI as GUI
import matplotlib

from utils.GUI import Application

matplotlib.use('Agg')   # or 'SVG', etc.
import matplotlib.pyplot as plt
import math

def main():
    # Load configs
    cube_cfg = cfg.cube.heavy
    pop_cfg  = cfg.population.large
    scale_cfg= cfg.scale.cube_scale

    # Simulate
    pop = Population(cube_cfg, pop_cfg, scale_cfg, seed=42)
    pop.simulate()

    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), gridspec_kw={'hspace': 0.4})
    pop.plot_true_weights(ax=axes[0])
    pop.plot_measured_weights(ax=axes[1])
    pop.plot_errors(ax=axes[2])
    # Optionally, add a footer or text box

    pop_size_txt = pop_cfg.population_size
    
    if pop_size_txt > 9999:
        exp = int(math.log10(pop_size_txt))
        mant = pop_size_txt / (10 ** exp)
        # Display integer mantissa if possible
        mant_str = str(int(mant)) if mant.is_integer() else f"{mant:.2f}"
        size_str = f"${mant_str}\\times10^{{{exp}}}$"
    else:
        size_str = str(pop_size_txt)

    cfg_text = (
        f"Cube base weight: {cube_cfg.base_weight}{cube_cfg.base_weight_unit}\n"
        f"Cube tolerance: {cube_cfg.part_tolerance}{cube_cfg.tolerance_unit}\n"
        f"Population config: {size_str}\n"
        f"Scale config: {scale_cfg.scale_error}{scale_cfg.scale_error_unit}\n"
    )
    # Place a text box in the lower center
    fig.text(
        0.95, 0.95, cfg_text,
        ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.5)
    )

    plt.subplots_adjust(top=0.85, bottom=0.1)

    App = GUI.Application(fig)
    App.mainloop()


if __name__ == '__main__':
    main()
