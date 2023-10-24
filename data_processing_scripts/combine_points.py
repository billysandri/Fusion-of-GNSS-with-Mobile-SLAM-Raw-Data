import os
import pandas as pd
import sys

def process_subfolder(subfolder):
    point_csv = os.path.join(subfolder, "point.csv")
    fused_csv = os.path.join(subfolder, "fused_points.csv")
    device_csv = os.path.join(subfolder, "device_points.csv")

    if os.path.exists(point_csv) and os.path.exists(fused_csv) and os.path.exists(device_csv):
        # Read the CSV files into DataFrames
        point_df = pd.read_csv(point_csv)
        fused_df = pd.read_csv(fused_csv)
        device_df = pd.read_csv(device_csv)

        # Create a new DataFrame with the desired columns
        new_df = pd.DataFrame({
            "peg_id": range(1, len(point_df) + 1),
            "f_easting": fused_df["x"],
            "f_northing": fused_df["y"],
            "f_elevation": fused_df["z"],
            "f_horizontal_acc": fused_df["horizontalAccuracy"],
            "f_vertical_acc": fused_df["verticalAccuracy"],
            "d_easting": device_df["x"],
            "d_northing": device_df["y"],
            "d_elevation": device_df["z"],
            "d_horizontal_acc": device_df["horizontalAccuracy"],
            "d_vertical_acc": device_df["verticalAccuracy"],
            "w_easting": point_df["x"],
            "w_northing": point_df["y"],
            "w_elevation": point_df["z"],
            "w_horizontal_acc": point_df["horizontalAccuracy"],
            "w_vertical_acc": point_df["verticalAccuracy"]
        })

        # Save the new DataFrame to a CSV file in the same subfolder
        new_csv = os.path.join(subfolder, "point_data.csv")
        new_df.to_csv(new_csv, index=False)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    for root, _, _ in os.walk(folder_path):
        process_subfolder(root)

if __name__ == "__main__":
    main()
