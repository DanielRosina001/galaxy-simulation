import pandas as pd

def collate_csv_files(file_list, output_file):
    """
    Collates multiple CSV files with the same columns into one CSV file.
    
    Parameters:
    - file_list: List of file paths to the CSV files to combine.
    - output_file: Path to save the combined CSV file.
    """
    # Read and combine all CSV files
    combined_df = pd.concat([pd.read_csv(file) for file in file_list], ignore_index=True)
    
    # Save the combined dataframe to the output file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to: {output_file}")

# Example usage:
csv_files = ["galaxy_bar_stars.csv", "galaxy_bulge_stars.csv", "galaxy_disk_stars.csv", "galaxy_spiral_arms_stars.csv", "galaxy_scattered_stars.csv"]  # List of input CSV files
output_csv = "galaxy_stars.csv"  # Output file name

collate_csv_files(csv_files, output_csv)
