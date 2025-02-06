import numpy as np
import matplotlib.pyplot as plt
import csv

# Parameters
num_star_forming_regions = 50
stars_per_region = 20
galaxy_radius = 30000.0 
min_distance_between_regions = 1000.0
brightness = 2
size = 2


class star_formation_regions_render: 
    def __init__(self, num_star_forming_regions, stars_per_region, galaxy_radius, min_distance_between_regions, brightness, size):
        self.num_star_forming_regions = num_star_forming_regions
        self.stars_per_region = stars_per_region
        self.galaxy_radius = galaxy_radius
        self.min_distance_between_regions = min_distance_between_regions
        self.bright = brightness
        self.s = size
        self.points = self.generate_region_centers()
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_stars()
    
    def generate_region_centers(self):
        points = []
        
        while len(points) < self.num_star_forming_regions:
            # Generate a random point in Cartesian coordinates within the sphere
            x = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            y = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            z = np.random.uniform(-self.galaxy_radius, self.galaxy_radius)
            
            # Check if the point lies within the sphere
            if x**2 + y**2 + z**2 <= self.galaxy_radius**2 and x**2 + y**2 + z**2 >= self.min_distance_between_regions**2:
                new_point = np.array([x, y, z])
                # Check if the new point is at least min_distance from all existing points
                if all(np.linalg.norm(new_point - p) >= self.min_distance_between_regions for p in points):
                    points.append(new_point)
    
        return np.array(points)
    
    def generate_stars(self):
        x = []
        y = []
        z = []
        temperature = []
        brightness = []
        size = []

        for i in range(self.num_star_forming_regions):
            num_stars_in_region = int(np.round(np.random.normal(self.stars_per_region, 400)))

            max_radius = np.random.normal(2000, 10)

            center_translation = self.points[i]

            for _ in range(num_stars_in_region): 
                r = max_radius*2 / np.sqrt(np.random.uniform(0, 1) ** (-2/3) - 1) 
                theta = np.arccos(np.random.uniform(-1, 1))
                phi = 2 * np.pi * np.random.uniform(0, 1)
                x.append((r * np.sin(theta) * np.cos(phi) + np.random.normal(0, max_radius/20)) + center_translation[0])
                y.append((r * np.sin(theta) * np.sin(phi) + np.random.normal(0, max_radius/20)) + center_translation[1])
                z.append((r * np.cos(theta) + np.random.normal(0, max_radius/20)) + center_translation[2])
                temperature.append(np.random.normal(10000, 1500))
                #while temperature[i] < 3000: 
                #    temperature[i] = np.random.normal(3000, 100)
                #temperature[i] = int(np.fix(np.random.normal(1000,400)))
                brightness.append(self.bright)
                size.append(self.s)

        return np.array(x), np.array(y), np.array(z), np.array(temperature), np.array(brightness), np.array(size)
    
    def plot_star_formation_regions(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_ylim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_zlim(-self.galaxy_radius*2, self.galaxy_radius*2)
        ax.set_title('Star formation regions model')
        plt.show()
    
    def export(self, output_file = "star_formation_regions_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")
    

if __name__ == "__main__":
    star_formation_regions = star_formation_regions_render(num_star_forming_regions, stars_per_region, galaxy_radius, min_distance_between_regions, brightness, size)

    star_formation_regions.plot_star_formation_regions()
    star_formation_regions.export()
