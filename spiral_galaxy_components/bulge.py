import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from .config import BulgeParameters, default_bulge_parameters

@dataclass
class Bulge: 

    """Initialize bulge renderer with given parameters."""

    parameters: BulgeParameters = field(default_factory=lambda: deepcopy(default_bulge_parameters)) # Copy of default_bulge_parameters

    n_stars: int = field(init=False)
    bulge_radius: float = field(init=False)
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
        self.bulge_radius = self.parameters.bulge_radius
        self.temp_mean = self.parameters.temp_mean
        self.temp_sd = self.parameters.temp_sd
        self.brightness = self.parameters.brightness
        self.size = self.parameters.size

        print('\n---------- Bulge Rendering ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_galaxy_bulge()
        self.df = pd.DataFrame({
            'XX': self.XX/1000, 
            'YY': self.YY/1000, 
            'ZZ': self.ZZ/1000, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })

    def generate_galaxy_bulge(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        """
        Generate a spherical distribution of stars following a Plummer model.

        Parameters:
            n_stars (int): Number of stars to generate.
            scale_length (float): Scale length for the Plummer model.

        Returns:
            tuple: Arrays of x, y, z coordinates of stars.
        """

        x = np.zeros(self.n_stars)
        y = np.zeros(self.n_stars)
        z = np.zeros(self.n_stars)
        temperature = np.zeros(self.n_stars)
        brightness = np.zeros(self.n_stars)
        size = np.zeros(self.n_stars)

        print("\nGenerating bulge stars...")

        for i in tqdm(range(self.n_stars), desc="Generating bulge stars"):
            # Generate radius using the Plummer model
            r = self.bulge_radius / np.sqrt(np.random.uniform(0, 1) ** (-2/3) - 1) - 1
            while r > 4*self.bulge_radius: 
                r = self.bulge_radius / np.sqrt(np.random.uniform(0, 1) ** (-2/3) - 1) - 1

            # Generate random angles for spherical coordinates
            theta = np.arccos(2 * np.random.uniform(0, 1) - 1)  # Polar angle
            phi = 2 * np.pi * np.random.uniform(0, 1)           # Azimuthal angle

            # Convert spherical coordinates to Cartesian coordinates
            x[i] = r * np.sin(theta) * np.cos(phi) + np.random.normal(0, self.bulge_radius/20)
            y[i] = r * np.sin(theta) * np.sin(phi) + np.random.normal(0, self.bulge_radius/20)
            z[i] = r * np.cos(theta) + np.random.normal(0, self.bulge_radius/20)
            temperature[i] = np.random.normal(self.temp_mean, self.temp_sd)
            #while temperature[i] < 3000: 
            #    temperature[i] = np.random.normal(3000, 100)
            #temperature[i] = int(np.fix(np.random.normal(1000,400)))
            brightness[i] = self.brightness
            size[i] = self.size
        
        print()

        return x, y, z, temperature, brightness, size

    # Render Bulge
    def render(self) -> None:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from render import render_open3d
        render_open3d(self.df)

    # Export stars to a CSV file
    def export(self, output_file: str = "spiral_galaxy_bulge_stars.csv") -> None:
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")


if __name__ == "__main__":

    bulge = Bulge(default_bulge_parameters)

    bulge.render()
    # bulge.export()
