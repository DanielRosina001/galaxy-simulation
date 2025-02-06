import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy

# Parameters
n_stars = 3000  # Number of stars
bar_length = 8000.0   # Length scale for the bar tapering
#bar_dimensions = (1, 0.4, 0.3)

class bar_render: 
    def __init__(self, n_stars, bar_length):
        self.n_stars = n_stars
        self.bar_length = bar_length    
        self.x, self.y, self.z, self.temperature, self.brightness, self.size = self.generate_galaxy_bar()    

    def generate_galaxy_bar(self):
        """
        Generate the star positions in the galaxy bar.
        """
        # Generate x using a stretched Plummer distribution with tapering
        center_length = self.bar_length/2

        bar_thickness_y = self.bar_length*0.2  # Maximum radial distance in the y direction

        r_x = np.zeros(self.n_stars)
        for i in range(self.n_stars): 
            r_x[i] = np.random.normal(0,bar_thickness_y/2)


        theta_x = np.zeros(self.n_stars)
        for i in range(self.n_stars):
            theta_x[i] = np.random.uniform(0, 2*np.pi)

        x = np.zeros(self.n_stars)

        def x_distribution(x): 
            #return np.exp(-(x/bar_length)**2)  # Original sd=bar_length
            #return np.exp(-(2*x/bar_length)**2)  #sd = bar_length/2

            if x < -0.6*center_length: 
                return np.exp(-((x+0.6)/(center_length))**2)
            elif -0.6*center_length <= x <= 0.6*center_length:
                return 1
            else:
                return np.exp(-((x-0.6)/(center_length))**2) # middle 60% uniform and ends dropping off in terms of gaussian

        def x_candidate(lower_bound, upper_bound):
            for i in range(10000):
                x_candidate_value = np.random.uniform(lower_bound, upper_bound)
                candidate_prob = np.random.uniform(0, 1)
                if candidate_prob < x_distribution(x_candidate_value):
                    return x_candidate_value
                    break
            raise ValueError("Candidate not found")
        
        for i in range(self.n_stars):
            x[i] = x_candidate(-center_length, center_length)
        
        for i in range(self.n_stars):
            r_x[i] = r_x[i] * (1+(x[i]/(2*center_length))**2)**(-2.5) # x*center_length: the x represents speed of radius dropoff

        # Generate y and z with a cylindrical distribution
        y = np.zeros(self.n_stars)
        z = np.zeros(self.n_stars)
        for i in range(self.n_stars):
            y[i] = r_x[i] * np.cos(theta_x[i])
            z[i] = r_x[i] * np.sin(theta_x[i])*(3/4)
        
        temperature = np.zeros(self.n_stars)

        brightness = np.zeros(self.n_stars)

        size = np.zeros(self.n_stars)

        for i in range(self.n_stars):
            x[i] = x[i] + np.random.normal(0, bar_length/100)
            y[i] = y[i] + np.random.normal(0, bar_length/100)
            z[i] = z[i] + np.random.normal(0, bar_length/100)
            temperature[i] = 5000
            brightness[i] = 2
            size[i] = 2

        return x, y, z, temperature, brightness, size

    def plot_galaxy_bar(self):
        """
        Plot the galaxy bar in 3D.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.x, self.y, self.z, s=1, alpha=0.7)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-self.bar_length*1.5/2, self.bar_length*1.5/2)
        ax.set_ylim(-self.bar_length*1.5/2, self.bar_length*1.5/2)
        ax.set_zlim(-self.bar_length*1.5/2, self.bar_length*1.5/2)
        ax.set_title('Galaxy Bar model')
        plt.show()

    # Export stars to a CSV file
    def export(self, output_file = "galaxy_bar_stars.csv"): 
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i]/1000, self.y[i]/1000, self.z[i]/1000, self.temperature[i], self.brightness[i], self.size[i]])

        print(f"Stars exported to {output_file}")


bar = bar_render(n_stars, bar_length)

bar.plot_galaxy_bar()
bar.export()
