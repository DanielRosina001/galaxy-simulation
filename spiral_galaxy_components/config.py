from dataclasses import dataclass, field

@dataclass(frozen=True)
class BulgeParameters: 
    n_stars: int
    bulge_radius: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_bulge_parameters: BulgeParameters = BulgeParameters(
    n_stars=5000, 
    bulge_radius=0.8, 
    temp_mean=3000.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass(frozen=True)
class BarParameters: 
    n_stars: int
    bar_length: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_bar_parameters: BarParameters = BarParameters(
    n_stars=10000, 
    bar_length=8.0, 
    temp_mean=4500.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass(frozen=True)
class DiskParameters: 
    n_stars: int
    r0: float
    norm_height: float
    thin_height: float
    cutoff_radius: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_disk_parameters: DiskParameters = DiskParameters(
    n_stars=35000, 
    r0=5.0, 
    norm_height=0.6, 
    thin_height=0.1, 
    cutoff_radius=31.0, 
    temp_mean=6000.0, 
    temp_sd=500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass(frozen=True)
class SpiralArmParameters: 
    n_stars: int
    star_prop: tuple[float]
    num_main_arms: int
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
    n_stars=49000, 
    star_prop=(0.4,0.6), 
    num_main_arms=2, 
    num_secondary_arms=30, 
    r0=4.0, 
    k=0.23, 
    spiral_distribution=1.2, 
    z_distribution=0.1, 
    max_theta=8.90118, # 17*pi/6 
    temp_mean=9000.0, 
    temp_sd=1500.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass(frozen=True)
class ScatteredStarParameters: 
    n_stars: int
    galaxy_radius: float
    min_distance: float
    temp_mean: float
    temp_sd: float
    brightness: float
    size: float

default_scattered_stars_parameters: ScatteredStarParameters = ScatteredStarParameters(
    n_stars=1000, 
    galaxy_radius=30.0, 
    min_distance=0.03, 
    temp_mean=6000.0, 
    temp_sd=2000.0, 
    brightness=2.0, 
    size=2.0
)


@dataclass(frozen=True)
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