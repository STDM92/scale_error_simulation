from PIL.ImageOps import scale

from population import Population
import config as cfg

def main():
    cube_cfg = cfg.cube.heavy
    n = cfg.population.big
    scale_cfg = cfg.scale.cube_scale
    pop = Population(cube_cfg, n, scale_cfg)
    summary = pop.summary()
    print(f"Mean error: {summary['mean_err']:.4f}")
    print(f"Std error:  {summary['std_err']:.4f}")


if __name__ == "__main__":
    main()