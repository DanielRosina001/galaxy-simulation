import numpy as np
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm

# Parameters
mean_main_stars_per_arm = 20000
num_main_arms = 2
mean_secondary_stars_per_arm = 500
num_secondary_arms = 20
r0 = 4000.0           # Base radius
k = 0.23           # Tightness of the spiral
spiral_distribution = 1200.0   # Scale distribution by spiral arms
z_distribution = 100.0
max_theta = 17*np.pi/6

class spiral_arms_render:
    def __init__(self, mean_main_stars_per_arm, num_main_arms, mean_secondary_stars_per_arm, num_secondary_arms, r0, k, spiral_distribution, z_distribution, max_theta):
        self.mmspa = mean_main_stars_per_arm
        self.nma = num_main_arms
        self.msspa = mean_secondary_stars_per_arm
        self.nsa = num_secondary_arms
        self.r0 = r0
        self.k = k
        self.spiral_distribution = spiral_distribution
        self.z_distribution = z_distribution
        self.max_theta = max_theta
        self.x, self.y, self.z = self.generate_all_spiral_arms()
    
    def logarithmic_spiral(self, theta):
        """
        Calculate the radial distance for a logarithmic spiral.

        Parameters:
            theta (float or array): Angular coordinate in radians.
            r0 (float): Base radius of the spiral.
            k (float): Tightness parameter of the spiral.

        Returns:
            float or array: Radial distance corresponding to theta.
        """
        return self.r0 * np.exp(self.k * theta)
      
    def generate_main_arms(self):
        """
        Generate star positions in spiral arms.

        Returns:
            tuple: Arrays of x, y, z coordinates of stars. 
        """
        x = []
        y = []
        z = []

        for arm in range(self.nma): 
            stars_in_arm = self.mmspa + np.int64(np.floor(np.random.normal(0, self.mmspa/10)))
            hotspot_centers, hotspot_sds, max_d = self.hotspot_values_for_arm(np.random.randint(25,35), True)
            arm_theta_offset = (2 * np.pi / self.nma) * arm
            for _ in range(stars_in_arm): 
                while True: 
                    theta = (self.max_theta)**0.5 * np.random.uniform(0, self.max_theta)**0.5  # Spiral length (e.g., 2 full rotations)
                    
                    if self.density_function_for_arm(hotspot_centers, hotspot_sds, max_d, theta) < np.random.uniform(0,1): 
                        continue

                    r = self.logarithmic_spiral(theta)

                    x_star = r * np.cos(theta + arm_theta_offset)
                    y_star = r * np.sin(theta + arm_theta_offset)
                    
                    density = np.exp(-r/self.r0)
                    if density <= np.random.uniform(0,1): 
                        continue
                    else: 
                        break
                
                x.append(x_star + np.random.normal(0, self.spiral_distribution/2))
                y.append(y_star + np.random.normal(0, self.spiral_distribution/2))
                z.append(np.random.normal(0, self.z_distribution/2))
        
        return np.array(x), np.array(y), np.array(z)
    
    def theta_arm_offset(self): 
        def offset_function(theta): 
            for i in range(self.nma + 1): 
                ran_min = ((2*i-1)*2*np.pi)/(2 * self.nma)
                ran_max = ((2*i+1)*2*np.pi)/(2 * self.nma)
                if ran_min <= theta <= ran_max: 
                    return 1 - np.exp(-(theta - (2*np.pi*i/self.nma))**2 / (2 * (np.pi/(self.nma*2))**2))
        
        while True: 
            arm_theta_offset = np.random.uniform(0,2*np.pi)
            if offset_function(arm_theta_offset) < np.random.uniform(0,1): 
                continue
            return arm_theta_offset
        
    def hotspot_values_for_arm(self, num_of_hotspots, main): 
        distance = self.max_theta/(num_of_hotspots+1)
        hotspot_centers = []
        if main: 
            min_theta = 0
            mean_range = distance/50
            sd_range = distance*2
        else: 
            min_theta = 2*self.max_theta/3
            mean_range = distance
            sd_range = distance/4
        temp_centers = list(np.linspace(min_theta, self.max_theta, num_of_hotspots))
        for i in temp_centers: 
            hotspot_centers.append(i + np.random.normal(0, mean_range/2))
        hotspot_sds = []
        for _ in range(num_of_hotspots): 
            hotspot_sds.append(np.random.uniform(0, sd_range/2))
        
        def density_function(theta): 
            total = 0
            for i in range(len(hotspot_centers)):
                total += np.exp(-(theta-hotspot_centers[i])**2 / (2 * hotspot_sds[i]**2))
            return total
        
        temp = np.linspace(0,self.max_theta, 100)
        max_d = 0
        for i in temp: 
            d = density_function(i)
            if d>max_d: 
                max_d = d

        return hotspot_centers, hotspot_sds, max_d
        
    def density_function_for_arm(self, hotspot_centers, hotspot_sds, max_d, theta):
        def density_function(theta): 
            total = 0
            for i in range(len(hotspot_centers)):
                total += np.exp(-(theta-hotspot_centers[i])**2 / (2 * hotspot_sds[i]**2))
            return total

        final_density = density_function(theta)/max_d

        return final_density

    def generate_secondary_arms(self): 
        x = []
        y = []
        z = []

        for arm in range(self.nsa): 
            stars_in_arm = self.msspa + np.int64(np.floor(np.random.normal(0, self.msspa/10)))
            hotspot_centers, hotspot_sds, max_d = self.hotspot_values_for_arm(np.random.randint(1,7), False)
            arm_theta_offset = self.theta_arm_offset()
            for _ in range(stars_in_arm): 
                while True: 
                    theta = (self.max_theta)**0.5 * np.random.uniform(0, self.max_theta)**0.5  # Spiral length (e.g., 2 full rotations)
                    
                    if self.density_function_for_arm(hotspot_centers, hotspot_sds, max_d, theta) < np.random.uniform(0,1): 
                        continue

                    r = self.logarithmic_spiral(theta)

                    x_star = r * np.cos(theta + arm_theta_offset)
                    y_star = r * np.sin(theta + arm_theta_offset)
                    
                    density = np.exp(-r/self.r0)
                    if density <= np.random.uniform(0,1): 
                        continue
                    else: 
                        break
                
                x.append(x_star + np.random.normal(0, self.spiral_distribution/4))
                y.append(y_star + np.random.normal(0, self.spiral_distribution/4))
                z.append(np.random.normal(0, self.z_distribution/2))
        
        return np.array(x), np.array(y), np.array(z)
    
    def generate_all_spiral_arms(self): 
        main_x, main_y, main_z = self.generate_main_arms()
        secondary_x, secondary_y, secondary_z = self.generate_secondary_arms()
        
        x = np.concatenate((main_x, secondary_x))
        y = np.concatenate((main_y, secondary_y))
        z = np.concatenate((main_z, secondary_z))

        return x, y, z

    def plot_spiral_arms(self):
        """
        Plot the spiral arms in 3D.

        Parameters:
            x, y, z (arrays): Coordinates of stars.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.r0*10, self.r0*10)
        ax.set_ylim(-self.r0*10, self.r0*10)
        ax.set_zlim(-self.r0*10, self.r0*10)
        ax.set_title('Spiral Arms of the Galaxy')
        plt.show()
    
    def export(self, output_file = "galaxy_spiral_arms_stars.csv"):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["x", "y", "z"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i], self.y[i], self.z[i]])

        print(f"Stars exported to {output_file}")

        return output_file
    

spiral_arms = spiral_arms_render(mean_main_stars_per_arm, num_main_arms, mean_secondary_stars_per_arm, num_secondary_arms, r0, k, spiral_distribution, z_distribution, max_theta)

spiral_arms.plot_spiral_arms()
spiral_arms.export()
            
