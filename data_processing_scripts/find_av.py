import os
import sys
import pandas as pd
import numpy as np

# Check for the correct number of command line arguments
if len(sys.argv) != 2:
    print("Usage: python script.py /path/to/root/folder")
    sys.exit(1)

root_folder = sys.argv[1]

# Function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2 + (p1['z'] - p2['z'])**2)

# Function to find the closest row to a given point in the dataframe
def find_closest_point(point, df):
    distances = df.apply(lambda row: euclidean_distance(point, row), axis=1)
    closest_row = df.loc[distances.idxmin()]
    return closest_row

# Recurse through all subfolders
for subdir, dirs, files in os.walk(root_folder):
    for file in files:
        if file.lower().endswith('.csv'):
            file_path = os.path.join(subdir, file)
            if "range" in file.lower():
                print(f"Processing 'range' file: {file_path}")
                range_df = pd.read_csv(file_path)
                for index, row in range_df.iterrows():
                    start = row['start']
                    end = row['end']
                    
                    # Find the corresponding "world" CSV file
                    world_file = None
                    for world_file_candidate in files:
                        if "world" in world_file_candidate.lower():
                            world_file = os.path.join(subdir, world_file_candidate)
                            break
                    
                    if world_file:
                        print(f"Processing 'world' file: {world_file}")
                        world_df = pd.read_csv(world_file)
                        
                        # Filter rows in the "world" CSV based on the id range
                        filtered_world_df = world_df[(world_df['id'] >= start) & (world_df['id'] <= end)]
                        
                        if not filtered_world_df.empty:
                            # Calculate the average of x, y, z values
                            average_point = filtered_world_df[['x', 'y', 'z']].mean()
                            print(f"Average point for range {start}-{end}: {average_point}")
                            
                            # Find the closest row in "world" CSV to the average point
                            closest_row = find_closest_point(average_point, filtered_world_df)
                            print(f"Closest row for range {start}-{end}: {closest_row.to_dict()}")
                            
                            # Create the output CSV file for "point" in the same subfolder
                            output_file = os.path.join(subdir, "point.csv")
                            
                            # Check if the file already exists
                            if os.path.exists(output_file):
                                # Append the closest row to the existing "point.csv"
                                point_df = pd.read_csv(output_file)
                                point_df = pd.concat([point_df, closest_row.to_frame().T], ignore_index=True)
                            else:
                                # Create a new "point.csv" file
                                point_df = closest_row.to_frame().T
                            
                            # Save the "point" DataFrame to the CSV file in the same subfolder
                            point_df.to_csv(output_file, index=False)
                            print(f"Closest points saved to {output_file}")
