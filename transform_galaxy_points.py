import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import scipy

galaxy = pd.read_csv('galaxy_stars.csv')
center_location = np.load('galaxy_center_locations.npy')

x = galaxy['XX']
y = galaxy['YY']
z = galaxy['ZZ']

def rotation(x_in, y_in, z_in): 
    galaxy = np.vstack((x_in, y_in, z_in))
    phi = np.random.uniform(0, 2 * np.pi)
    cos_theta = np.random.uniform(-1, 1)
    theta = np.arccos(cos_theta)

    R_z = np.array([
        [np.cos(phi), -np.sin(phi), 0],
        [np.sin(phi), np.cos(phi), 0],
        [0, 0, 1]
    ])
    
    R_y = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    
    R = np.dot(R_z, R_y)

    rotated_galaxy = np.dot(R, galaxy)

    x_out = rotated_galaxy[0]
    y_out = rotated_galaxy[1]
    z_out = rotated_galaxy[2]

    return x_out, y_out, z_out

x_r, y_r, z_r = rotation(x, y, z)

def translate(x_in, y_in, z_in, i): 
    translation = center_location[i]
    x_out = []
    y_out = []
    z_out = []
    for j in range(len(x_in)): 
        x_out.append(x_in[j] + translation[0])
        y_out.append(y_in[j] + translation[1])
        z_out.append(z_in[j] + translation[2])
    return x_out, y_out, z_out

x_t, y_t, z_t = translate(x_r, y_r, z_r, 0)

galaxy['XX'] = x_t
galaxy['YY'] = y_t
galaxy['ZZ'] = z_t

def export(output_file = "galaxy_stars_rotated.csv"): 
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["XX", "YY", "ZZ", "T", "B", "S"])
        for i in range(len(galaxy["XX"])):
            writer.writerow([galaxy["XX"][i], galaxy['YY'][i], galaxy["ZZ"][i], galaxy["T"][i], galaxy["B"][i], galaxy["S"][i]])

    print(f"Stars exported to {output_file}")

export()
