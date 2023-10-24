import pandas as pd
import argparse
import os

# Define the command-line argument for the input folder
parser = argparse.ArgumentParser(description='Recursively add an "id" column to all CSV files in a folder and its subfolders.')
parser.add_argument('input_folder', help='Input folder containing CSV files')

# Parse the command-line argument
args = parser.parse_args()

# Iterate through all CSV files in the input folder and its subfolders
for root, _, files in os.walk(args.input_folder):
    for csv_file in files:
        if csv_file.endswith('.csv'):
            input_file = os.path.join(root, csv_file)
            output_file = os.path.join(root, f"{os.path.splitext(csv_file)[0]}_id.csv")

            # Load the CSV into a DataFrame
            df = pd.read_csv(input_file)

            # Add a new column 'id' at index 0 with row numbers
            df.insert(0, 'id', range(1, len(df) + 1))

            # Save the updated DataFrame to a new CSV file in the same subfolder
            df.to_csv(output_file, index=False)

            print(f"Added 'id' column to {input_file} and saved as {output_file}.")
