from simulation.population import Population
import config as cfg
import matplotlib.pyplot as plt

def main():

    # --- Load configuration ---
    cube_cfg = cfg.cube.heavy
    n = cfg.population.big
    scale_cfg = cfg.scale.cube_scale

    # --- Create population object ---
    pop = Population(cube_cfg, n, scale_cfg)

    # --- Print Mean and Std Error ---
    summary = pop.summary()
    print(f"Mean error: {summary['mean_err']:.4f}")
    print(f"Std error:  {summary['std_err']:.4f}")

    # --- Plot Charts for true weights, measured weights and error distribution ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))
    pop.plot_true_weights(ax=ax1)
    pop.plot_measured_weights(ax=ax2)
    pop.plot_errors(ax=ax3)




if __name__ == "__main__":
    main()