# Galaxy_Simulation_Project
## A program that can generate simulated galaxies using star values stored in a CSV file
This program uses probability distributions and established properties of real-life galaxies to generate points in a simulated one, containing features that real ones would have such as the disk, bulge, and randomly scattered stars. Running this program would generate a CSV file with 6 columns: XX, YY, ZZ, T, B, S. XX, YY, ZZ refer to the (x,y,z) coordinates of the given star in parsecs. T refers to the temperature of the star in Kelvin, B refers to the brightness of the star, and S refers to the star's size. 

### Example of a simulated galaxy: 
![Spiral Galaxy Simulation Example](SpiralGalaxyExample.jpg)

### Example usage: 
```bash
python3 spiral_galaxy_rendering/spiral_galaxy_rendering.py
Stars exported to spiral_galaxy_stars.csv
```

To view as in the picture above, upload the CSV file to paraview, then use the Table to Points function to convert it to an image. Select 'XX', 'YY', and 'ZZ' for the coordinates and set the color parameter to 'T' on a red-blue scale. 