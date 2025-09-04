import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from spiral_galaxy_components.config import SpiralArmParameters, default_spiral_arm_parameters
from spiral_galaxy_components.helper import *

import time


@dataclass
class SpiralArms:
    """Initialize spiral arm renderer with given parameters."""

    parameters: SpiralArmParameters = field(default_factory=lambda: deepcopy(default_spiral_arm_parameters)) # Copy of default_spiral_arm_parameters

    n_stars: int = field(init=False)
    star_prop: tuple[float] = field(init=False)
    num_main_arms: int = field(init=False)
    num_secondary_arms: int = field(init=False)
    r0: float = field(init=False)
    k: float = field(init=False)
    spiral_distribution: float = field(init=False)
    z_distribution: float = field(init=False)
    max_theta: float = field(init=False)
    temp_mean: float = field(init=False)
    temp_sd: float = field(init=False)
    brightness: float = field(init=False)
    size: float = field(init=False)

    XX: np.ndarray = field(init=False) # Units: pc
    YY: np.ndarray = field(init=False) # Units: pc
    ZZ: np.ndarray = field(init=False) # Units: pc
    T: np.ndarray = field(init=False)
    B: np.ndarray = field(init=False)
    S: np.ndarray = field(init=False)
    df: pd.DataFrame = field(init=False) # Units: kpc

    def __post_init__(self) -> None: 

        self.n_stars = self.parameters.n_stars
        self.star_prop = self.parameters.star_prop
        self.num_main_arms = self.parameters.num_main_arms
        self.num_secondary_arms = self.parameters.num_secondary_arms
        self.r0 = self.parameters.r0
        self.k = self.parameters.k
        self.spiral_distribution = self.parameters.spiral_distribution
        self.z_distribution = self.parameters.z_distribution
        self.max_theta = self.parameters.max_theta
        self.temp_mean = self.parameters.temp_mean
        self.temp_sd = self.parameters.temp_sd
        self.brightness = self.parameters.brightness
        self.size = self.parameters.size

        print('\n---------- Spiral Arms Generation ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_spiral_arms()
        self.df = pd.DataFrame({
            'XX': self.XX, 
            'YY': self.YY, 
            'ZZ': self.ZZ, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })
    
    def __logarithmic_spiral(self, theta: float) -> float:
        """Calculate radius for given theta values using logarithmic spiral formula."""
        return self.r0 * np.exp(self.k * theta)
    
    def sample_hotspot(self, offset_theta: float, mean_theta: float, sd_theta: float, num_stars: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Sample stars for a blob."""
        theta = np.random.normal(mean_theta, sd_theta, num_stars)
        r = self.__logarithmic_spiral(theta)
        x = r * np.cos(theta + offset_theta)
        y = r * np.sin(theta + offset_theta)
        z = np.random.normal(0, self.z_distribution/2, num_stars)
        return x, y, z, r, theta

    def generate_arm_star_locations(self, main_arm: bool, 
                           num_stars: int, 
                           theta_offset: float, 
                           num_hotspots: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate stars for a single spiral arm."""
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        r: list[float] = []
        theta: list[float] = []
        
        if main_arm: 
            mean_theta = np.linspace(0, self.max_theta, num_hotspots) + np.random.normal(0, self.max_theta/10, num_hotspots)
            sd_theta = np.random.uniform(self.max_theta/50, self.max_theta/10, num_hotspots)
        else: 
            mean_theta = np.linspace(0, self.max_theta, num_hotspots) + np.random.normal(0, self.max_theta/10, num_hotspots)
            sd_theta = np.random.uniform(self.max_theta/1000, self.max_theta/20, num_hotspots)
        num_stars_ls = uneven_div(num_stars, num_hotspots, 0.5)

        pbar = tqdm(total=num_stars, desc=f"Generating {'main' if main_arm else 'secondary'} arm stars", leave=False)

        for i in range(num_hotspots):

            mean_theta_i = mean_theta[i]
            sd_theta_i = sd_theta[i]
            num_stars_i = num_stars_ls[i]

            x_temp, y_temp, z_temp, r_temp, theta_temp = self.sample_hotspot(theta_offset, mean_theta_i, sd_theta_i, num_stars_i)

            x.extend(x_temp + np.random.normal(0, self.spiral_distribution/2, num_stars_i))
            y.extend(y_temp + np.random.normal(0, self.spiral_distribution/2, num_stars_i))
            z.extend(z_temp)

            theta.extend(theta_temp)
            r.extend(r_temp)
            
            pbar.update(num_stars_i)
        
        pbar.close()
        
        return np.array(x), np.array(y), np.array(z), np.array(r), np.array(theta)
    
    def generate_spiral_arms(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate all spiral arms."""
    

        print("\nStarting spiral arms generation...")

        pbar = tqdm(total=self.num_main_arms, desc="Main arms progress")

        prop = proportional_div(self.n_stars, self.star_prop)
        num_main_stars, num_secondary_stars = prop[0], prop[1]
        num_main_stars_ls = even_div(num_main_stars, self.num_main_arms)
        num_secondary_stars_ls = even_div(num_secondary_stars, self.num_secondary_arms)
        
        main_theta_offsets = [(2 * np.pi / self.num_main_arms) * arm for arm in range(self.num_main_arms)]
        secondary_theta_offsets = [(2 * np.pi / self.num_secondary_arms) * arm for arm in range(self.num_secondary_arms)]

        x_all = []
        y_all = []
        z_all = []

        main_times: np.ndarray = np.zeros(self.num_main_arms)
        secondary_times: np.ndarray = np.zeros(self.num_secondary_arms)

        print(f"\nGenerating {self.num_main_arms} main spiral arms...")

        for i in range(self.num_main_arms):

            start_time = time.time()

            stars_in_arm = num_main_stars_ls[i]
            theta_offset = main_theta_offsets[i]

            x, y, z, _, _ = self.generate_arm_star_locations(True, stars_in_arm, theta_offset, np.random.randint(25, 35))
            
            x_all.extend(list(x))
            y_all.extend(list(y))
            z_all.extend(list(z))

            main_times[i] = time.time() - start_time

            pbar.update(1)

        pbar.close()

        print(f"Average time per arm: {np.mean(main_times):.2f} seconds")
        print(f"Total time taken: {np.sum(main_times):.2f} seconds")

        print(f"\nGenerating {self.num_secondary_arms} main spiral arms...")

        for i in range(self.num_secondary_arms):

            start_time = time.time()

            stars_in_arm = num_secondary_stars_ls[i]
            theta_offset = secondary_theta_offsets[i]

            x, y, z, _, _ = self.generate_arm_star_locations(False, stars_in_arm, theta_offset, np.random.randint(8, 12))
            
            x_all.extend(list(x))
            y_all.extend(list(y))
            z_all.extend(list(z))

            secondary_times[i] = time.time() - start_time

            pbar.update(1)

        pbar.close()

        print(f"Average time per arm: {np.mean(main_times):.2f} seconds")
        print(f"Total time taken: {np.sum(main_times):.2f} seconds")

        print("\nCombining all spiral arms...\n")
        
        temperature = np.random.normal(self.temp_mean, self.temp_sd, self.n_stars)
        brightness = np.full(self.n_stars, self.brightness)
        size = np.full(self.n_stars, self.size)
        
        return x_all, y_all, z_all, temperature, brightness, size
        
    # Render Spiral Arms
    def render(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from render import render_open3d
        render_open3d(self.df)

    # Export stars to a CSV file
    def export(self, output_file = "spiral_galaxy_spiral_arm_stars.csv"):
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")


def main(): 
    spiral_arms = SpiralArms(default_spiral_arm_parameters)

    spiral_arms.render()
    
    e = input("Export stars? (y/n): ")
    if e.lower() == 'y': 
        spiral_arms.export()

if __name__ == "__main__":
    main()