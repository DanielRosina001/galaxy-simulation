import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from colour_rendering.temp_to_rgb import temp_to_rgb

class SmearedGalaxy: 

    def __init__(self, input_file, pixels, kernel_size=15, kernel_sd=2, normalization='none', log_factor=50, gamma=0.4): 
        self.stars = pd.read_csv(input_file)
        self.pixels = pixels
        CC = [temp_to_rgb(temp, out_fmt='rgb') for temp in self.stars['T']]
        
        max_x = max(abs(max(list(self.stars['XX']))), abs(min(list(self.stars['XX']))))
        max_y = max(abs(max(list(self.stars['YY']))), abs(min(list(self.stars['YY']))))

        max_dist = np.ceil(max(max_x, max_y))

        unit_length = max_dist*2 / self.pixels

        self.grid = np.zeros((self.pixels,self.pixels))

        self.color_grid = np.zeros((self.pixels,self.pixels,3), dtype=float)

        for row in range(len(self.stars['XX'])): 
            star = self.stars.iloc[row]
            rgb = CC[row]
            
            cell_x = int(np.floor(star['XX'] / unit_length) + self.pixels//2)
            cell_y = int(np.floor(star['YY'] / unit_length) + self.pixels//2)

            self.grid[cell_y, cell_x] += star['B']

            for i in range(0,3): self.color_grid[cell_y, cell_x, i] += rgb[i]
        
        if normalization == 'none': 
            pass
        elif normalization == 'log': 
            self.grid = self.normalize_log(arr=self.grid, factor=log_factor)
        elif normalization == 'gamma': 
            self.grid = self.gamma_correction(self.grid, gamma=gamma)

        
        self.gaussian_smearing = self.gaussian_kernel(kernel_size, kernel_sd)
        
    def smear_grid(self) -> None: 
        self.convolved_grid = scipy.signal.convolve2d(self.grid, self.gaussian_smearing, mode='same', boundary='symm')
        convolved_channels = [
            scipy.ndimage.convolve(self.color_grid[:, :, i], self.gaussian_smearing, mode='reflect') 
            for i in range(3)
        ]
        self.convolved_color_grid = np.stack(convolved_channels, axis=-1)

    def normalize_log(self, arr, factor):
        return np.log1p(arr * factor) / np.log1p(factor)
    
    def gamma_correction(self, arr, gamma):
        return np.power(arr, gamma)

    def gaussian_kernel(self, size, sigma):
        x = np.linspace(-size // 2, size // 2, size)
        y = np.linspace(-size // 2, size // 2, size)
        X, Y = np.meshgrid(x, y)
        kernel = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
        return 1.2*kernel / kernel.sum()  # Normalize the kernel
    
    def plot(self, color: bool =True): 
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        if color: 
            plt.imshow(self.color_grid, origin='lower')
        else: 
            plt.imshow(self.grid, cmap='gray', origin='lower')
        plt.title("Original Image")

        # plt.subplot(1, 2, 2)
        # plt.imshow(self.convolved_grid, cmap='gray', origin='lower')
        # plt.title("Convolved Grid")
        plt.subplot(1, 2, 2)
        if color: 
            plt.imshow(self.convolved_color_grid, origin='lower')
        else: 
            plt.imshow(self.convolved_grid, cmap='gray', origin='lower')
        plt.title("Convolved Image")

        plt.show()

if __name__ == '__main__': 
    galaxy = SmearedGalaxy(input_file='examples/spiral_galaxy_stars.csv', 
                           pixels=1024, 
                           kernel_size=10, 
                           kernel_sd=0.5, 
                           normalization='none', 
                           log_factor=10, 
                           gamma=0.4)
    galaxy.smear_grid()
    galaxy.plot(color=True)









