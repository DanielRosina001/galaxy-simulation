import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_points_within_sphere(radius, n_points, min_distance):
    points = []
    
    while len(points) < n_points:
        # Generate a random point in Cartesian coordinates within the sphere
        x = np.random.uniform(-radius, radius)
        y = np.random.uniform(-radius, radius)
        z = np.random.uniform(-radius, radius)
        
        # Check if the point lies within the sphere
        if x**2 + y**2 + z**2 <= radius**2 and x**2 + y**2 + z**2 >= min_distance**2:
            new_point = np.array([x, y, z])
            # Check if the new point is at least min_distance from all existing points
            if all(np.linalg.norm(new_point - p) >= min_distance for p in points):
                points.append(new_point)
    
    return np.array(points)

def plot_points_in_sphere(points):
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=10, color='blue', alpha=0.6)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    ax.set_title("Random Points Within a Sphere")
    plt.show()

# Parameters
sphere_radius = 1000000.0
num_points = 50
min_distance = 100000.0

# Generate points
points = generate_points_within_sphere(sphere_radius, num_points, min_distance)

# Plot the points
plot_points_in_sphere(points)

np.save('galaxy_center_locations.npy', points)
