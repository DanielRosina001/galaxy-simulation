import numpy as np
import matplotlib.pyplot as plt
import csv
from bulge_rendering import bulge_render
from bar_rendering import bar_render
from disk_rendering import disk_render
from spiral_arms_rendering import spiral_arms_render
from scattered_stars_rendering import scattered_stars_render

class SpiralGalaxy:
    def __init__(self, 
                 n_bulge_stars = 3000, # Bulge parameters
                 bulge_radius = 800.0, 

                 n_bar_stars = 3000, # Bar parameters
                 bar_length = 8000.0, 

                 n_disk_stars = 25000, # Disk parameters
                 r0 = 4000, 
                 scale_height = 600, 
                 cutoff_radius = 31000, 

                 mean_main_stars_per_arm = 6000, # Spiral arm parameters
                 num_main_arms = 2, 
                 mean_secondary_stars_per_arm = 500, 
                 num_secondary_arms = 30, 
                 k = 0.23, 
                 spiral_distribution = 1200.0, 
                 z_distribution = 100.0, 
                 max_theta = 17 * np.pi / 6, 
                 
                 galaxy_radius = 30000.0, # Scattered stars parameters
                 n_scattered_stars = 100, 
                 min_distance = 30.0
                 ):
        
        self.brightness = 2
        self.size = 2

        # Bulge parameters
        self.n_bulge_stars = n_bulge_stars
        self.bulge_radius = bulge_radius
        # Bar parameters
        self.n_bar_stars = n_bar_stars
        self.bar_length = bar_length
        # Disk parameters
        self.n_disk_stars = n_disk_stars
        self.r0 = r0
        self.scale_height = scale_height
        self.cutoff_radius = cutoff_radius
        # Spiral arms parameters
        self.mean_main_stars_per_arm = mean_main_stars_per_arm
        self.num_main_arms = num_main_arms
        self.mean_secondary_stars_per_arm = mean_secondary_stars_per_arm
        self.num_secondary_arms = num_secondary_arms
        self.k = k
        self.spiral_distribution = spiral_distribution
        self.z_distribution = z_distribution
        self.max_theta = max_theta
        # Scattered stars parameters
        self.galaxy_radius = galaxy_radius
        self.n_scattered_stars = n_scattered_stars
        self.min_distance = min_distance



    def generate_galaxy(self): 

        self.bulge = bulge_render(self.n_bulge_stars, 
                                  self.bulge_radius, 
                                  self.brightness, 
                                  self.size)
        self.bar = bar_render(self.n_bar_stars, 
                              self.bar_length, 
                              self.brightness, 
                              self.size)
        self.disk = disk_render(self.n_disk_stars, 
                                self.r0, 
                                self.scale_height, 
                                self.cutoff_radius, 
                                self.brightness, 
                                self.size)
        self.spiral_arms = spiral_arms_render(self.mean_main_stars_per_arm, 
                                              self.num_main_arms, 
                                              self.mean_secondary_stars_per_arm, 
                                              self.num_secondary_arms, 
                                              self.r0, 
                                              self.k, 
                                              self.spiral_distribution, 
                                              self.z_distribution, 
                                              self.max_theta, 
                                              self.brightness, 
                                              self.size)
        self.scattered_stars = scattered_stars_render(self.galaxy_radius, 
                                                      self.n_scattered_stars, 
                                                      self.min_distance, 
                                                      self.brightness, 
                                                      self.size)

        self.x = np.concatenate([self.bulge.x, self.bar.x, self.disk.x, self.spiral_arms.x, self.scattered_stars.x])
        self.y = np.concatenate([self.bulge.y, self.bar.y, self.disk.y, self.spiral_arms.y, self.scattered_stars.y])
        self.z = np.concatenate([self.bulge.z, self.bar.z, self.disk.z, self.spiral_arms.z, self.scattered_stars.z])
        self.temperature = np.concatenate([self.bulge.temperature, self.bar.temperature, self.disk.temperature, self.spiral_arms.temperature, self.scattered_stars.temperature])
        self.brightness = np.concatenate([self.bulge.brightness, self.bar.brightness, self.disk.brightness, self.spiral_arms.brightness, self.scattered_stars.brightness])
        self.size = np.concatenate([self.bulge.size, self.bar.size, self.disk.size, self.spiral_arms.size, self.scattered_stars.size])

    def export(self, output_file="spiral_galaxy_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i], self.y[i], self.z[i], self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")

if __name__ == "__main__":
    spiral_galaxy = SpiralGalaxy()
    spiral_galaxy.generate_galaxy()
    spiral_galaxy.export()