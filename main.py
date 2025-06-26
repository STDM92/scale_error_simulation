from simulation.population import Population
import config as cfg
import matplotlib.pyplot as plt

from utils.console_style import add_plot_to_pdf_bootstrap


def main():

    # --- Load configuration ---
    cube_cfg = cfg.cube.heavy
    pop_config = cfg.population.large
    scale_cfg = cfg.scale.cube_scale

    # --- Create population object and simulate population ---
    pop = Population(cube_cfg, pop_config, scale_cfg, seed=42)
    pop.simulate()

    # --- Print Mean and Std Error ---
    """summary = pop.summary()
    print(f"Mean error: {summary['mean_err']:.4f}")
    print(f"Std error:  {summary['std_err']:.4f}")"""

    # --- Plot Charts for true weights, measured weights and error distribution ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12), gridspec_kw={'hspace': 0.4})
    pop.plot_true_weights(ax=ax1)
    pop.plot_measured_weights(ax=ax2)
    pop.plot_errors(ax=ax3)

    plt.subplots_adjust( top=0.9)


    add_plot_to_pdf_bootstrap(fig)

    plt.show()




if __name__ == "__main__":
    main()