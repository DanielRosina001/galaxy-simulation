import numpy as np
import pandas as pd
import os
from copy import deepcopy
from dataclasses import dataclass, field
from spiral_galaxy_components.bulge import Bulge
from spiral_galaxy_components.bar import Bar
from spiral_galaxy_components.disk import Disk
from spiral_galaxy_components.spiral_arms import SpiralArms
from spiral_galaxy_components.scattered_stars import ScatteredStars
from spiral_galaxy_components.config import *


@dataclass
class SpiralGalaxy:

    config: SpiralGalaxyConfig = field(default_factory=lambda: deepcopy(default_config))

    bulge_parameters: BulgeParameters = field(init=False)
    bar_parameters: BarParameters = field(init=False)
    disk_parameters: DiskParameters = field(init=False)
    spiral_arm_parameters: SpiralArmParameters = field(init=False)
    scattered_stars_parameters: ScatteredStarParameters = field(init=False)

    bulge: Bulge = field(init=False)
    bar: Bar = field(init=False)
    disk: Disk = field(init=False)
    spiral_arms: SpiralArms = field(init=False)
    scattered_stars: ScatteredStars = field(init=False)

    XX: np.ndarray = field(init=False) 
    YY: np.ndarray = field(init=False) 
    ZZ: np.ndarray = field(init=False) 
    T: np.ndarray = field(init=False)
    B: np.ndarray = field(init=False)
    S: np.ndarray = field(init=False)
    df: pd.DataFrame = field(init=False) 


    def __post_init__(self) -> None: 
        print('\n------------- SPIRAL GALAXY GENERATION ------------\n')

        # Bulge parameters
        self.bulge_parameters = self.config.bulge_parameters

        # Bar parameters
        self.bar_parameters = self.config.bar_parameters

        # Disk parameters
        self.disk_parameters = self.config.disk_parameters

        # Spiral arms parameters
        self.spiral_arm_parameters = self.config.spiral_arm_parameters

        # Scattered stars parameters
        self.scattered_stars_parameters = self.config.scattered_stars_parameters

    def generate_galaxy(self) -> None: 

        self.bulge = Bulge(self.bulge_parameters)

        self.bar = Bar(self.bar_parameters)

        self.disk = Disk(self.disk_parameters)

        self.spiral_arms = SpiralArms(self.spiral_arm_parameters)

        self.scattered_stars = ScatteredStars(self.scattered_stars_parameters)
        
        self.XX = np.concatenate([self.bulge.XX, self.bar.XX, self.disk.XX, self.spiral_arms.XX, self.scattered_stars.XX])
        self.YY = np.concatenate([self.bulge.YY, self.bar.YY, self.disk.YY, self.spiral_arms.YY, self.scattered_stars.YY])
        self.ZZ = np.concatenate([self.bulge.ZZ, self.bar.ZZ, self.disk.ZZ, self.spiral_arms.ZZ, self.scattered_stars.ZZ])
        self.T = np.concatenate([self.bulge.T, self.bar.T, self.disk.T, self.spiral_arms.T, self.scattered_stars.T])
        self.B = np.concatenate([self.bulge.B, self.bar.B, self.disk.B, self.spiral_arms.B, self.scattered_stars.B])
        self.S = np.concatenate([self.bulge.S, self.bar.S, self.disk.S, self.spiral_arms.S, self.scattered_stars.S])

        self.df = pd.DataFrame({
            'XX': self.XX, 
            'YY': self.YY, 
            'ZZ': self.ZZ, 
            'T': self.T, 
            'B': self.B, 
            'S': self.S
        })

    # Render Galaxy
    def render(self) -> None:
        from render import render_open3d
        render_open3d(self.df)

    # Export stars to a CSV file
    def export(self, output_file: str = "spiral_galaxy_stars.csv") -> None:
        if output_file[-4:] != '.csv': 
            output_file += '.csv'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        self.df.to_csv(output_path, index=False)

        print(f"Stars exported to {output_path}")


def main(): 
    spiral_galaxy = SpiralGalaxy()

    spiral_galaxy.generate_galaxy()
    spiral_galaxy.render()

    e = input("Export stars? (y/n): ")
    if e.lower() == 'y': 
        spiral_galaxy.export()

if __name__ == "__main__":
    main()