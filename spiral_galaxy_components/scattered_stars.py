import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from spiral_galaxy_components.config import ScatteredStarParameters, default_scattered_stars_parameters


@dataclass
class ScatteredStars: 

    """Initialize scattered star renderer with given parameters."""

    parameters: ScatteredStarParameters = field(default_factory=lambda: deepcopy(default_scattered_stars_parameters)) # Copy of default_scattered_stars_parameters

    n_stars: int = field(init=False)
    galaxy_radius: float = field(init=False)
    min_distance: float = field(init=False)
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
        self.galaxy_radius = self.parameters.galaxy_radius
        self.min_distance = self.parameters.min_distance
        self.temp_mean = self.parameters.temp_mean
        self.temp_sd = self.parameters.temp_sd
        self.brightness = self.parameters.brightness
        self.size = self.parameters.size

        print('\n---------- Scattered Stars Rendering ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_scattered_stars()
        self.df = pd.DataFrame({
            'XX': self.XX/1000, 
            'YY': self.YY/1000, 
            'ZZ': self.ZZ/1000, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })

    def generate_scattered_stars(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate scattered stars within a spherical volume."""
        x = []
        y = []
        z = []
        temperature = []
        brightness = []
        size = []
        
        print("\nGenerating scattered stars...")
        for _ in tqdm(range(self.n_stars), desc="Generating scattered stars"):
            phi = np.random.uniform(0, 2 * np.pi)
            cos_theta = np.random.uniform(-1, 1)
            theta = np.arccos(cos_theta)
            r = np.random.normal(40000, 13333)
            x_c = r * np.sin(theta) * np.cos(phi)
            y_c = r * np.sin(theta) * np.sin(phi)
            z_c = r * np.cos(theta)

            x.append(x_c)
            y.append(y_c)
            z.append(z_c)
            temperature.append(np.random.normal(self.temp_mean, self.temp_sd))
            brightness.append(self.brightness)
            size.append(self.size)
        
        print()

        return np.array(x), np.array(y), np.array(z), np.array(temperature), np.array(brightness), np.array(size)

    # Render Scattered Stars
    def render(self) -> None:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from render import render_open3d
        render_open3d(self.df)
        
    # Export stars to a CSV file
    def export(self, output_file: str = "spiral_galaxy_scattered_stars.csv") -> None:
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")


if __name__ == "__main__":
    scattered_stars = ScatteredStars(default_scattered_stars_parameters)

    scattered_stars.render()
    # scattered_stars.export()



