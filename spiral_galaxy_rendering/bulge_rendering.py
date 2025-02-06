import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy

class bulge_render: 
    def __init__(self, # Parameters
                 n_stars = 3000, 
                 bulge_radius = 800.0, 
                 brightness = 2, 
                 size = 2):
        self.n_stars = n_stars
        self.bulge_radius = bulge_radius 
        self.bright = brightness
        self.s = size
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_galaxy_bulge()


    def generate_galaxy_bulge(self):
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

        for i in range(self.n_stars):
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
            temperature[i] = np.random.normal(3000, 100)
            #while temperature[i] < 3000: 
            #    temperature[i] = np.random.normal(3000, 100)
            #temperature[i] = int(np.fix(np.random.normal(1000,400)))
            brightness[i] = self.bright
            size[i] = self.s

        return x, y, z, temperature, brightness, size

    def plot_galaxy_bulge(self):
        """
        Plot the galaxy bulge in 3D.

        Parameters:
            x, y, z (arrays): Coordinates of stars.
        """
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.bulge_radius*2, self.bulge_radius*2)
        ax.set_ylim(-self.bulge_radius*2, self.bulge_radius*2)
        ax.set_zlim(-self.bulge_radius*2, self.bulge_radius*2)
        ax.set_title('Galaxy Bulge model')
        plt.show()

    # Export stars to a CSV file
    def export(self, output_file = "galaxy_bulge_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")


if __name__ == "__main__":
    bulge = bulge_render()

    bulge.plot_galaxy_bulge()
    bulge.export()
