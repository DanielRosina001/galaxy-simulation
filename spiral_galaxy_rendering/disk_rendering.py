import numpy as np
import matplotlib.pyplot as plt
import csv

# Parameters
num_stars = 25000    # Total number of stars
r0 = 4000   # Scale length for the radial density
scale_height = 600    # Scale height for the z-distribution
cutoff_radius = 31000 # Maximum radius of the galactic disk
brightness = 2
size = 2
'''
# Generate galactic disk stars
x, y, z = generate_galactic_disk(num_stars, r0, scale_height, cutoff_radius)

# Plot the galactic disk
plot_galactic_disk(x, y, z)

# Export stars to a CSV file
'''

class disk_render:
    def __init__(self, num_stars, r0, scale_height, cutoff_radius, brightness, size): 
        self.num_stars = num_stars
        self.r0 = r0
        self.scale_height = scale_height
        self.cutoff_radius = cutoff_radius
        self.bright = brightness
        self.s = size
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_galactic_disk()
    
    def generate_galactic_disk(self):
        """
        Generate star positions for the general galactic disk.

        Parameters:
            num_stars (int): Total number of stars to generate.
            scale_length (float): Scale length for the radial density distribution (in same units as cutoff_radius).
            scale_height (float): Scale height for the vertical distribution (standard deviation of z-coordinates).
            cutoff_radius (float): Maximum radial extent of the disk.

        Returns:
            tuple: Arrays of x, y, z coordinates of stars.
        """
        x = []
        y = []
        z = []
        temperature = np.zeros(self.num_stars)
        brightness = np.zeros(self.num_stars)
        size = np.zeros(self.num_stars)

        for i in range(self.num_stars):
            # Generate radial distance r with exponential distribution
            '''
            while True:
                r = np.random.uniform(0, cutoff_radius)
                probability = np.exp(- r / r0) * r
                if np.random.uniform(0, 1) < probability / (cutoff_radius * np.exp(-cutoff_radius / r0)):
                    break
            
            while True:
                r = np.random.exponential(r0)
                if r <= cutoff_radius:
                    break
            '''
            while True:
                x_star = np.random.uniform(-self.cutoff_radius, self.cutoff_radius)
                y_star = np.random.uniform(-self.cutoff_radius, self.cutoff_radius)
                r = np.sqrt(x_star ** 2 + y_star ** 2)
                if r > self.cutoff_radius: 
                    continue
                density = np.exp(-r/self.r0)
                if density > np.random.uniform(0,1): 
                    break

            # Generate z-coordinate from a Gaussian distribution
            z_star = np.random.normal(0, self.scale_height/2)

            x.append(x_star)
            y.append(y_star)
            z.append(z_star)
            temp = np.random.normal(5000, 100)
            temperature[i] = temp
            brightness[i] = self.bright
            size[i] = self.s

        return np.array(x), np.array(y), np.array(z), temperature, brightness, size
    
    def plot_galactic_disk(self):
        """
        Plot the galactic disk in 3D.

        Parameters:
            x, y, z (arrays): Coordinates of stars.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.01)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.cutoff_radius, self.cutoff_radius)
        ax.set_ylim(-self.cutoff_radius, self.cutoff_radius)
        ax.set_zlim(-self.cutoff_radius, self.cutoff_radius)
        ax.set_title('Galactic Disk model')
        plt.show()
    
    def export(self, output_file = "galaxy_disk_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")

        return output_file
    

if __name__ == "__main__":
    disk = disk_render(num_stars, r0, scale_height, cutoff_radius, brightness, size)

    disk.plot_galactic_disk()
    disk.export()

