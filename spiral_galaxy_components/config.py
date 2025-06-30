from dataclasses import dataclass

@dataclass
class BulgeParameters: 
    n_stars: int
    bulge_radius: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_bulge_parameters: BulgeParameters = BulgeParameters(
    n_stars=3000, 
    bulge_radius=800.0, 
    temp_mean=3000.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass
class BarParameters: 
    n_stars: int
    bar_length: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_bar_parameters: BarParameters = BarParameters(
    n_stars=5000, 
    bar_length=8000.0, 
    temp_mean=4500.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass
class DiskParameters: 
    n_stars: int
    r0: float
    scale_height: float
    thin_height: float
    cutoff_radius: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_disk_parameters: DiskParameters = DiskParameters(
    n_stars=15000, 
    r0=4000.0, 
    scale_height=600.0, 
    thin_height=100.0, 
    cutoff_radius=31000.0, 
    temp_mean=6000.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass
class SpiralArmParameters: 
    mean_main_stars_per_arm: int
    num_main_amrs: int
    mean_secondary_stars_per_arm: int
    num_secondary_arms: int
    r0: float
    k: float
    spiral_distribution: float
    z_distribution: float
    max_theta: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_spiral_arm_parameters: SpiralArmParameters = SpiralArmParameters(
    mean_main_stars_per_arm=6000,
    num_main_amrs=2, 
    mean_secondary_stars_per_arm=500, 
    num_secondary_arms=30, 
    r0=4000.0, 
    k=0.23, 
    spiral_distribution=1200.0, 
    z_distribution=100.0, 
    max_theta=8.90118, # 17*pi/6 
    temp_mean=9000.0, 
    temp_sd=1500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass
class ScatteredStarParameters: 
    n_stars: int
    galaxy_radius: float
    min_distance: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_scattered_stars_parameters: ScatteredStarParameters = ScatteredStarParameters(
    n_stars=500, 
    galaxy_radius=30000.0, 
    min_distance=30.0, 
    temp_mean=6000.0, 
    temp_sd=2000.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass
class SpiralGalaxyConfig: 
    bulge_parameters: BulgeParameters
    bar_parameters: BarParameters
    disk_parameters: DiskParameters
    spiral_arm_parameters: SpiralArmParameters
    scattered_stars_parameters: ScatteredStarParameters

default_config: SpiralGalaxyConfig = SpiralGalaxyConfig(
    
    bulge_parameters=default_bulge_parameters, 

    bar_parameters=default_bar_parameters, 

    disk_parameters=default_disk_parameters, 

    spiral_arm_parameters=default_spiral_arm_parameters, 

    scattered_stars_parameters=default_scattered_stars_parameters

)