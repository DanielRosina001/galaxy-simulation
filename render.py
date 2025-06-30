import open3d as o3d
import pandas as pd
import numpy as np
from colour_rendering.temp_to_rgb import temp_to_rgb

def render_open3d(stars: pd.DataFrame) -> None: 
    # Extract coordinates and temperature
    points = stars[['XX', 'YY', 'ZZ']].values

    # Convert temperatures to colors for each temperature
    CC = [temp_to_rgb(temp, out_fmt='rgb') for temp in stars['T']]

    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(CC)

    # Set up a visualizer with black background and small point size
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='Stars', width=1024, height=768)
    vis.add_geometry(pcd)

    # Customize rendering
    render_option = vis.get_render_option()
    render_option.background_color = np.array([0, 0, 0])  # Black background
    render_option.point_size = 1.0  # Smaller point size for finer stars
    render_option.show_coordinate_frame = False  # Hide XYZ axes

    # Run visualizer
    vis.run()
    vis.destroy_window()


def render_open3d_file(file_dir: str) -> None: 
    # Load CSV
    stars = pd.read_csv(file_dir)

    # Render DF
    render_open3d(stars)



if __name__ == '__main__': 
    import sys

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    elif len(sys.argv) == 1:
        file_path = input("Enter the relative path to the file you want to view: ").strip()
    else: 
        raise ValueError("Usage: python render.py <path_to_csv_file>")
    
    csv_path = sys.argv[1]
    render_open3d_file(file_dir=csv_path)