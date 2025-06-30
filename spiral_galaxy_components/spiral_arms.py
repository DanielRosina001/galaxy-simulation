import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from spiral_galaxy_components.config import SpiralArmParameters, default_spiral_arm_parameters


@dataclass
class SpiralArms:
    
    """Initialize spiral arm renderer with given parameters."""

    parameters: SpiralArmParameters = field(default_factory=lambda: deepcopy(default_spiral_arm_parameters)) # Copy of default_spiral_arm_parameters

    mean_main_stars_per_arm: int = field(init=False)
    num_main_amrs: int = field(init=False)
    mean_secondary_stars_per_arm: int = field(init=False)
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

        self.mean_main_stars_per_arm = self.parameters.mean_main_stars_per_arm
        self.num_main_amrs = self.parameters.num_main_amrs
        self.mean_secondary_stars_per_arm = self.parameters.mean_secondary_stars_per_arm
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

        print('\n---------- Spiral Arms Rendering ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_all_spiral_arms()
        self.df = pd.DataFrame({
            'XX': self.XX/1000, 
            'YY': self.YY/1000, 
            'ZZ': self.ZZ/1000, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })
    
    def __logarithmic_spiral(self, theta: float) -> float:
        """Calculate radius for given theta values using logarithmic spiral formula."""
        return self.r0 * np.exp(self.k * theta)
    
    def hotspot_values_for_arm(self, num_of_hotspots: int, main: bool) -> tuple[list[float], list[float], float]:
        """Generate hotspot values for spiral arms."""
        distance = self.max_theta / (num_of_hotspots + 1)
        
        if main:
            min_theta = 0.0
            mean_range = distance/50
            sd_range = distance*2
        else:
            min_theta = 2*self.max_theta/3
            mean_range = distance
            sd_range = distance/4
            
        # Generate hotspot centers with random offsets
        temp_centers = np.linspace(min_theta, self.max_theta, num_of_hotspots)
        hotspot_centers = temp_centers + np.random.normal(0, mean_range/2, num_of_hotspots)
        hotspot_sds = np.random.uniform(0, sd_range/2, num_of_hotspots)
        
        # Calculate maximum density
        theta_test = np.linspace(0, self.max_theta, 100)
        densities = np.sum([np.exp(-(theta_test[:, np.newaxis] - hotspot_centers)**2 / 
                                 (2 * hotspot_sds**2))], axis=1)
        max_d = np.max(densities)
        
        return list(hotspot_centers), list(hotspot_sds), max_d

    def density_function_for_arm(self, hotspot_centers: list[float], hotspot_sds: list[float], 
                               max_d: float, theta: float) -> float:
        """Calculate density for a given theta position."""
        total = np.sum([np.exp(-(theta - center)**2 / (2 * sd**2)) 
                       for center, sd in zip(hotspot_centers, hotspot_sds)])
        return total / max_d

    def main_arm_density_array(self) -> np.ndarray | None:
        """Generate smoothed density array for main arms."""
        num_points = 10000
        random_values = np.random.rand(num_points)
        rect_kernel = np.ones(1500) / 1500  # Rectangular function
        
        smoothed_values = np.convolve(random_values, rect_kernel, mode='same')[1001:9001]
        smoothed_values = (smoothed_values - np.min(smoothed_values))
        smoothed_values /= np.max(smoothed_values)
        
        return smoothed_values

    def main_arm_random_density(self, smoothed_values: np.ndarray | None) -> float:
        """Generate random theta value based on density distribution."""
        if smoothed_values is None: 
            return -1.0
        else: 
            while True:
                n = np.random.randint(0, 8000)
                if smoothed_values[n] > np.random.uniform(0, 1):
                    return n * self.max_theta / 8000

    def generate_arm_stars(self, stars_in_arm: int, 
                           arm_theta_offset: float, 
                           hotspot_centers: list[float], 
                           hotspot_sds: list[float], 
                           max_d: float, 
                           is_main_arm: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate stars for a single spiral arm."""
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        num_stars: int = 0
        smoothed_values = self.main_arm_density_array() if is_main_arm else None
        
        pbar = tqdm(total=stars_in_arm, desc=f"Generating {'main' if is_main_arm else 'secondary'} arm stars", 
                   leave=False)
        
        # Add attempt counter per star
        max_attempts_per_star = 10000 if is_main_arm else 5000
        attempts = 0
        
        while num_stars < stars_in_arm:
            attempts += 1
            if attempts > max_attempts_per_star:
                # If we've tried too many times for this star, relax the constraints
                theta = np.random.uniform(0, self.max_theta)
                r = self.__logarithmic_spiral(theta)
                x_star = r * np.cos(theta + arm_theta_offset)
                y_star = r * np.sin(theta + arm_theta_offset)
                
                x.append(x_star + np.random.normal(0, self.spiral_distribution/2))
                y.append(y_star + np.random.normal(0, self.spiral_distribution/2))
                z.append(np.random.normal(0, self.z_distribution/2))
                pbar.update(1)
                num_stars += 1
                attempts = 0  # Reset for next star
                continue
                
            if is_main_arm and smoothed_values is not None:
                theta = self.main_arm_random_density(smoothed_values)
                if theta < 0.0: 
                    raise ValueError('smoothed_values is None')
                theta = (self.max_theta)**0.5 * theta**0.5
            else:
                theta = (self.max_theta)**0.5 * np.random.uniform(0, self.max_theta)**0.5
                
            if self.density_function_for_arm(hotspot_centers, hotspot_sds, max_d, theta) < np.random.uniform(0, 1):
                continue
                
            r = self.__logarithmic_spiral(theta)
            x_star = r * np.cos(theta + arm_theta_offset)
            y_star = r * np.sin(theta + arm_theta_offset)
            
            density = np.exp(-r/self.r0)
            if density <= np.random.uniform(0, 1):
                continue
                
            sigma = self.spiral_distribution / (4 if not is_main_arm else 2)
            x.append(x_star + np.random.normal(0, sigma))
            y.append(y_star + np.random.normal(0, sigma))
            z.append(np.random.normal(0, self.z_distribution/2))
            pbar.update(1)
            num_stars += 1
            attempts = 0  # Reset for next star
            
        pbar.close()
        return np.array(x), np.array(y), np.array(z)

    def generate_main_arms(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate main spiral arms."""
        x_all: list[float] = []
        y_all: list[float] = []
        z_all: list[float] = []
        
        print(f"\nGenerating {self.num_main_amrs} main spiral arms...")
        for arm in tqdm(range(self.num_main_amrs), desc="Main arms progress"):
            stars_in_arm = self.mean_main_stars_per_arm + int(np.floor(np.random.normal(0, self.mean_main_stars_per_arm/10)))
            hotspot_centers, hotspot_sds, max_d = self.hotspot_values_for_arm(np.random.randint(25, 35), True)
            arm_theta_offset = (2 * np.pi / self.num_main_amrs) * arm
            
            x, y, z = self.generate_arm_stars(stars_in_arm, arm_theta_offset, 
                                            hotspot_centers, hotspot_sds, max_d, True)
            x_all.extend(x)
            y_all.extend(y)
            z_all.extend(z)
        
        temperature = np.random.normal(self.temp_mean, self.temp_sd, len(x_all))
        brightness = np.full_like(x_all, self.brightness)
        size = np.full_like(x_all, self.size)
        
        return np.array(x_all), np.array(y_all), np.array(z_all), temperature, brightness, size

    def theta_arm_offset(self) -> float:
        """Calculate theta offset for secondary arms."""
        def offset_function(theta):
            for i in range(self.num_main_amrs + 1):
                ran_min = ((2*i-1)*2*np.pi)/(2 * self.num_main_amrs)
                ran_max = ((2*i+1)*2*np.pi)/(2 * self.num_main_amrs)
                if ran_min <= theta <= ran_max:
                    return 1 - np.exp(-(theta - (2*np.pi*i/self.num_main_amrs))**2 / (2 * (np.pi/(self.num_main_amrs*4))**2))
            return 0
        
        while True:
            arm_theta_offset = np.random.uniform(0, 2*np.pi)
            if offset_function(arm_theta_offset) < np.random.uniform(0, 1):
                continue
            return arm_theta_offset

    def generate_secondary_arms(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate secondary spiral arms."""
        x_all: list[float] = []
        y_all: list[float] = []
        z_all: list[float] = []
        
        print(f"\nGenerating {self.num_secondary_arms} secondary spiral arms...")
        for _ in tqdm(range(self.num_secondary_arms), desc="Secondary arms progress"):
            stars_in_arm = self.mean_secondary_stars_per_arm + int(np.floor(np.random.normal(0, self.mean_secondary_stars_per_arm/10)))
            hotspot_centers, hotspot_sds, max_d = self.hotspot_values_for_arm(np.random.randint(1, 5), False)
            arm_theta_offset = self.theta_arm_offset()
            
            x, y, z = self.generate_arm_stars(stars_in_arm, arm_theta_offset, 
                                            hotspot_centers, hotspot_sds, max_d, False)
            x_all.extend(x)
            y_all.extend(y)
            z_all.extend(z)
        
        temperature = np.random.normal(self.temp_mean, self.temp_sd, len(x_all))
        brightness = np.full_like(x_all, self.brightness)
        size = np.full_like(x_all, self.size)
        
        return np.array(x_all), np.array(y_all), np.array(z_all), temperature, brightness, size

    def generate_all_spiral_arms(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate all spiral arms (main and secondary)."""
        print("\nStarting spiral arms generation...")
        main_x, main_y, main_z, main_temp, main_bright, main_size = self.generate_main_arms()
        secondary_x, secondary_y, secondary_z, secondary_temp, secondary_bright, secondary_size = self.generate_secondary_arms()
        
        print("\nCombining all spiral arms...\n")
        return (np.concatenate((main_x, secondary_x)),
                np.concatenate((main_y, secondary_y)),
                np.concatenate((main_z, secondary_z)),
                np.concatenate((main_temp, secondary_temp)),
                np.concatenate((main_bright, secondary_bright)),
                np.concatenate((main_size, secondary_size)))

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

if __name__ == "__main__":
    spiral_arms = SpiralArms(default_spiral_arm_parameters)

    spiral_arms.render()
    # spiral_arms.export()
