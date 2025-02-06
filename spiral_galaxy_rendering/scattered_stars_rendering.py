import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D

class scattered_stars_render: 
    def __init__(self, # Parameters
                 galaxy_radius = 30000.0, 
                 num_stars = 100, 
                 min_distance = 30.0, 
                 brightness = 2, 
                 size = 2): 
        self.galaxy_radius = galaxy_radius
        self.num_stars = num_stars
        self.min_distance = min_distance
        self.bright = brightness
        self.s = size
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_points_within_sphere()

    def generate_points_within_sphere(self):

        points = []

        x = []
        y = []
        z = []
        temperature = []
        brightness = []
        size = []
        
        for _ in range(self.num_stars): 
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
            temperature.append(np.random.normal(5000, 100))
            brightness.append(self.bright)
            size.append(self.s)
        
        return np.array(x), np.array(y), np.array(z), np.array(temperature), np.array(brightness), np.array(size)

    def plot_points_in_sphere(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=10, color='blue', alpha=0.6)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.set_title("Random Points Within a Sphere")
        plt.show()
    
    def export(self, output_file = "galaxy_scattered_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")


if __name__ == "__main__":
    scattered_stars = scattered_stars_render()

    scattered_stars.plot_points_in_sphere()
    scattered_stars.export()



