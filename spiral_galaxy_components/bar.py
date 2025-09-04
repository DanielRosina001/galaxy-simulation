import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from .config import BarParameters, default_bar_parameters

# bar twice as long


@dataclass
class Bar: 

    """Initialize bar renderer with given parameters."""

    parameters: BarParameters = field(default_factory=lambda: deepcopy(default_bar_parameters)) # Copy of default_bar_parameters

    n_stars: int = field(init=False)
    bar_length: float = field(init=False)
    temp_mean: float = field(init=False)
    temp_sd: float = field(init=False)
    brightness: float = field(init=False)
    size: float = field(init=False)

    XX: np.ndarray = field(init=False)
    YY: np.ndarray = field(init=False)
    ZZ: np.ndarray = field(init=False)
    T: np.ndarray = field(init=False)
    B: np.ndarray = field(init=False)
    S: np.ndarray = field(init=False)
    df: pd.DataFrame = field(init=False)

    def __post_init__(self) -> None: 

        self.n_stars = self.parameters.n_stars
        self.bar_length = self.parameters.bar_length
        self.temp_mean = self.parameters.temp_mean
        self.temp_sd = self.parameters.temp_sd
        self.brightness = self.parameters.brightness
        self.size = self.parameters.size

        print('\n---------- Bar Rendering ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_galaxy_bar()
        self.df = pd.DataFrame({
            'XX': self.XX, 
            'YY': self.YY, 
            'ZZ': self.ZZ, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })

    def generate_galaxy_bar(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate the star positions in the galaxy bar.
        """
        # Generate x using a stretched Plummer distribution with tapering
        center_length = self.bar_length/2

        bar_thickness_y = self.bar_length*0.2  # Maximum radial distance in the y direction

        r_x = np.zeros(self.n_stars)
        theta_x = np.zeros(self.n_stars)
        x = np.zeros(self.n_stars)
        y = np.zeros(self.n_stars)
        z = np.zeros(self.n_stars)
        temperature = np.zeros(self.n_stars)
        brightness = np.zeros(self.n_stars)
        size = np.zeros(self.n_stars)

        print("\nGenerating bar stars...")
        pbar = tqdm(total=self.n_stars, desc="Generating bar stars")
        
        for i in range(self.n_stars): 
            r_x[i] = np.random.normal(0, bar_thickness_y/2)
            theta_x[i] = np.random.uniform(0, 2*np.pi)

        def x_distribution(x: float) -> float: 
            #return np.exp(-(x/bar_length)**2)  # Original sd=bar_length
            #return np.exp(-(2*x/bar_length)**2)  #sd = bar_length/2


            # Double check
            if x < -0.6*center_length: 
                return np.exp(-((x+0.6)/(center_length))**2)
            elif -0.6*center_length <= x <= 0.6*center_length:
                return 1.0
            else:
                return np.exp(-((x-0.6)/(center_length))**2) # middle 60% uniform and ends dropping off in terms of gaussian

        def x_candidate(lower_bound: float, upper_bound: float) -> float:
            max_attempts = 10000  # Add maximum attempts to prevent infinite loops
            attempts = 0
            while attempts < max_attempts:
                x_candidate_value = np.random.uniform(lower_bound, upper_bound)
                candidate_prob = np.random.uniform(0, 1)
                if candidate_prob < x_distribution(x_candidate_value):
                    return x_candidate_value
                attempts += 1
            # If max attempts reached, return a value from the center region
            return np.random.uniform(-0.6*center_length, 0.6*center_length)
        
        for i in range(self.n_stars):
            x[i] = x_candidate(-center_length, center_length)
            r_x[i] = r_x[i] * (1+(x[i]/(2*center_length))**2)**(-2.5) # x*center_length: the x represents speed of radius dropoff
            y[i] = r_x[i] * np.cos(theta_x[i])
            z[i] = r_x[i] * np.sin(theta_x[i])*(3/4)
            
            # Add position jitter and set properties
            x[i] = x[i] + np.random.normal(0, self.bar_length/100)
            y[i] = y[i] + np.random.normal(0, self.bar_length/100)
            z[i] = z[i] + np.random.normal(0, self.bar_length/100)
            temperature[i] = np.random.normal(self.temp_mean, self.temp_sd)
            brightness[i] = self.brightness
            size[i] = self.size
            
            pbar.update(1)
        
        pbar.close()
        print()

        return x, y, z, temperature, brightness, size

    # Render Bar
    def render(self) -> None:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from render import render_open3d
        render_open3d(self.df)

    # Export stars to a CSV file
    def export(self, output_file: str = "spiral_galaxy_bar_stars.csv") -> None:
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")


def main(): 
    bar = Bar(default_bar_parameters)

    bar.render()
    
    e = input("Export stars? (y/n): ")
    if e.lower() == 'y': 
        bar.export()

if __name__ == "__main__":
    main()