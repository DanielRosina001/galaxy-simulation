import numpy as np
import pandas as pd
import sys
import os
from tqdm import tqdm
from copy import deepcopy
from dataclasses import dataclass, field
from spiral_galaxy_components.config import DiskParameters, default_disk_parameters

# 10% extremely thin - 100 pc from side to side, magnetars

@dataclass
class Disk:

    """Initialize bar renderer with given parameters."""

    parameters: DiskParameters = field(default_factory=lambda: deepcopy(default_disk_parameters)) # Copy of default_disk_parameters

    n_stars: int = field(init=False)
    r0: float = field(init=False)
    norm_height: float = field(init=False)
    thin_height: float = field(init=False)
    cutoff_radius: float = field(init=False)
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
        self.r0 = self.parameters.r0
        self.norm_height = self.parameters.norm_height
        self.thin_height = self.parameters.thin_height
        self.cutoff_radius = self.parameters.cutoff_radius
        self.temp_mean = self.parameters.temp_mean
        self.temp_sd = self.parameters.temp_sd
        self.brightness = self.parameters.brightness
        self.size = self.parameters.size

        print('\n---------- Disk Rendering ----------')

        self.XX, self.YY, self.ZZ, self.T, self.B, self.S = self.generate_galaxy_disk()
        self.df = pd.DataFrame({
            'XX': self.XX, 
            'YY': self.YY, 
            'ZZ': self.ZZ, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })

    # def __generate_point_its(self) -> tuple[np.float64, np.float64, np.float64]: 
    #     """
    #     Generate a random point within the 3D space according to the density function through inverse transform sampling
    #     """
    #     # Sample phi uniformly
    #     phi = np.random.uniform(0, 2*np.pi, size=N)
    
    def generate_galaxy_disk(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate star positions for the general galactic disk.

        Parameters:
            n_stars (int): Total number of stars to generate.
            r0 (float): Scale length for the radial density distribution (in same units as cutoff_radius).
            norm_height (float): Scale height for standard vertical distribution (standard deviation of z-coordinates).
            thin_height (float): Scale height for thin vertical distribution (standard deviation of z-coordinates).
            cutoff_radius (float): Maximum radial extent of the disk.
        """
        x = []
        y = []
        z = []
        temperature = np.zeros(self.n_stars)
        brightness = np.zeros(self.n_stars)
        size = np.zeros(self.n_stars)

        print("\nGenerating disk stars...")
        pbar = tqdm(total=self.n_stars, desc="Generating disk stars")
        i = 0
        max_attempts = 1000  # Maximum attempts per star to prevent infinite loops
        
        n_thick_stars = int(self.n_stars * 0.9)
        while i < self.n_stars:
            if i < n_thick_stars: 
                scale_height = self.norm_height
            else: 
                scale_height = self.thin_height
            attempts = 0
            while attempts < max_attempts:
                x_star = np.random.uniform(-self.cutoff_radius, self.cutoff_radius)
                y_star = np.random.uniform(-self.cutoff_radius, self.cutoff_radius)
                r = np.sqrt(x_star ** 2 + y_star ** 2)
                if r > self.cutoff_radius: 
                    attempts += 1
                    continue
                density = np.exp2(-r/self.r0)
                if density > np.random.uniform(0,1): 
                    break
                attempts += 1
            
            # If we've exceeded max attempts, use a simpler method
            if attempts >= max_attempts:
                theta = np.random.uniform(0, 2*np.pi)
                r = np.random.uniform(0, self.cutoff_radius)
                x_star = r * np.cos(theta)
                y_star = r * np.sin(theta)

            # Generate z-coordinate from a Gaussian distribution
            z_star = np.random.normal(0, scale_height/2)

            x.append(x_star)
            y.append(y_star)
            z.append(z_star)
            temperature[i] = np.random.normal(self.temp_mean, self.temp_sd)
            brightness[i] = self.brightness
            size[i] = self.size
            
            pbar.update(1)
            i += 1

        pbar.close()
        print()

        return np.array(x), np.array(y), np.array(z), temperature, brightness, size
    
    # Render Disk
    def render(self) -> None:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from render import render_open3d
        render_open3d(self.df)
        
    # Export stars to a CSV file
    def export(self, output_file: str = "spiral_galaxy_disk_stars.csv") -> None:
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")
    

def main(): 
    disk = Disk(default_disk_parameters)

    disk.render()
    
    e = input("Export stars? (y/n): ")
    if e.lower() == 'y': 
        disk.export()

if __name__ == "__main__":
    main()