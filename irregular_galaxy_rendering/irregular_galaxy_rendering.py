import numpy as np
import matplotlib.pyplot as plt
import csv

# Parameters
num_star_forming_regions = 50
n_stars = 20000  
galaxy_radius = 30000.0 
min_distance_between_regions = 1000.0
size_ratio = (1, 0.9, 0.8)
brightness = 2
size = 2

class EllipticalGalaxy: 
    def __init__(self, n_stars, galaxy_radius, min_distance_between_regions, brightness, size):
        self.n_stars = n_stars
        self.galaxy_radius = galaxy_radius
        self.min_distance_between_regions = min_distance_between_regions
        self.bright = brightness
        self.s = size
        self.points = self.generate_region_centers
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_elliptical_galaxy()
    
    def generate_region_centers(self):
        points = []
        
        while len(points) < self.n_stars:
            # Generate a random point in Cartesian coordinates within the sphere
            x = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            y = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            z = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            
            # Check if the point lies within the sphere
            if x**2 + y**2 + z**2 <= self.galaxy_radius**2 and x**2 + y**2 + z**2 >= self.min_distance**2:
                new_point = np.array([x, y, z])
                # Check if the new point is at least min_distance from all existing points
                if all(np.linalg.norm(new_point - p) >= self.min_distance for p in points):
                    points.append(new_point)
    
        return np.array(points)
    
    def generate_star(self):
        x = np.zeros(self.n_stars)
        y = np.zeros(self.n_stars)
        z = np.zeros(self.n_stars)
        temperature = np.zeros(self.n_stars)
        brightness = np.zeros(self.n_stars)
        size = np.zeros(self.n_stars)
        normalized_ratio = tuple(i/max(size_ratio) for i in size_ratio)

        for i in range(self.n_stars):
            # Generate radius using the Plummer model
            r = self.galaxy_radius / np.sqrt(np.random.uniform(0, 1) ** (-2/3) - 1) - 1
            while r > self.galaxy_radius: 
                r = self.galaxy_radius / np.sqrt(np.random.uniform(0, 1) ** (-2/3) - 1) - 1

            # Generate random angles for spherical coordinates
            theta = np.arccos(2 * np.random.uniform(0, 1) - 1)  # Polar angle
            phi = 2 * np.pi * np.random.uniform(0, 1)           # Azimuthal angle

            # Convert spherical coordinates to Cartesian coordinates
            x[i] = (r * np.sin(theta) * np.cos(phi) + np.random.normal(0, self.galaxy_radius/20)) * normalized_ratio[0]
            y[i] = (r * np.sin(theta) * np.sin(phi) + np.random.normal(0, self.galaxy_radius/20)) * normalized_ratio[1]
            z[i] = (r * np.cos(theta) + np.random.normal(0, self.galaxy_radius/20)) * normalized_ratio[2]
            temperature[i] = np.random.normal(3000, 500)
            #while temperature[i] < 3000: 
            #    temperature[i] = np.random.normal(3000, 100)
            #temperature[i] = int(np.fix(np.random.normal(1000,400)))
            brightness[i] = self.bright
            size[i] = self.s

        return x, y, z, temperature, brightness, size
    
    def plot_elliptic_galaxy(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_ylim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_zlim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_title('Galaxy Bulge model')
        plt.show()
    
    def export(self, output_file = "elliptical_galaxy_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")
    

if __name__ == "__main__":
    elliptical_galaxy = EllipticalGalaxy(n_stars, galaxy_radius, brightness, size)

    elliptical_galaxy.plot_elliptic_galaxy()
    elliptical_galaxy.export()
