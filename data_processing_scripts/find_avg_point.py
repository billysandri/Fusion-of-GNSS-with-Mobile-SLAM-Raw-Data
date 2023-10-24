import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def find_closest_point(df, avg_x, avg_y, avg_z):
    df = df.copy()  # Create a copy to avoid the SettingWithCopyWarning
    df.loc[:, 'distance'] = ((df['x'] - avg_x) ** 2 + (df['y'] - avg_y) ** 2 + (df['z'] - avg_z) ** 2) ** 0.5
    closest_row = df.loc[df['distance'].idxmin()]
    return closest_row

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        range_files = [file for file in files if "range" in file and file.endswith(".csv")]
        
        for range_file in range_files:
            range_file_path = os.path.join(root, range_file)
            world_files = [file for file in files if "world" in file and file.endswith(".csv")]
            
            if not world_files:
                logging.warning(f"No world files found for {range_file_path}. Skipping.")
                continue

            range_df = pd.read_csv(range_file_path)
            
            for world_file in world_files:
                world_file_path = os.path.join(root, world_file)
                world_df = pd.read_csv(world_file_path)

                for index, row in range_df.iterrows():
                    start = row['start']
                    end = row['end']

                    relevant_world_rows = world_df[(world_df['id'] >= start) & (world_df['id'] <= end)]

                    if not relevant_world_rows.empty:
                        avg_x = relevant_world_rows['x'].mean()
                        avg_y = relevant_world_rows['y'].mean()
                        avg_z = relevant_world_rows['z'].mean()

                        closest_point = find_closest_point(relevant_world_rows, avg_x, avg_y, avg_z)

                        output_csv = os.path.join(root, "point.csv")
                        closest_point.to_csv(output_csv, index=False)
                        logging.info(f"Processed {range_file_path} and saved point.csv")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
    else:
        folder_path = sys.argv[1]
        process_folder(folder_path)
