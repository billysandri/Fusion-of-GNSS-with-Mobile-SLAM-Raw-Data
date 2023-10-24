import os
import pandas as pd

def find_closest_row(df, target_time):
    # Find the row with the closest timeStampTick to the target_time
    closest_row = df.iloc[(df['timeStampTick'] - target_time).abs().idxmin()]
    return closest_row

def process_subfolder(subfolder):
    point_file = os.path.join(subfolder, "point.csv")

    if os.path.isfile(point_file):
        device_df = None
        fused_df = None

        for file in os.listdir(subfolder):
            if file.startswith("aligned_device"):
                device_df = pd.read_csv(os.path.join(subfolder, file))
            elif file.startswith("fused"):
                fused_df = pd.read_csv(os.path.join(subfolder, file))

        if device_df is not None and fused_df is not None:
            device_points = pd.DataFrame(columns=device_df.columns)
            fused_points = pd.DataFrame(columns=fused_df.columns)

            point_df = pd.read_csv(point_file)

            for index, row in point_df.iterrows():
                target_time = int(row['timeStampTick'])
                closest_device_row = find_closest_row(device_df, target_time)
                closest_fused_row = find_closest_row(fused_df, target_time)

                device_points = pd.concat([device_points, closest_device_row.to_frame().T], ignore_index=True)
                fused_points = pd.concat([fused_points, closest_fused_row.to_frame().T], ignore_index=True)

            device_points.to_csv(os.path.join(subfolder, "device_points.csv"), index=False)
            fused_points.to_csv(os.path.join(subfolder, "fused_points.csv"), index=False)

def process_folder(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            process_subfolder(subfolder_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_folder>")
    else:
        input_folder = sys.argv[1]
        if os.path.exists(input_folder) and os.path.isdir(input_folder):
            process_folder(input_folder)
        else:
            print("Invalid directory path provided.")
