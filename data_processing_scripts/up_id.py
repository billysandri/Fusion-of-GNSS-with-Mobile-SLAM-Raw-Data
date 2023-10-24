import pandas as pd
import sys

def change_id_to_row_number(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Change the values in the 'id' column to row numbers
    df['id'] = df.index + 1
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_csv output_csv")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    
    change_id_to_row_number(input_csv, output_csv)
    
    print(f"Values in the 'id' column of '{input_csv}' have been changed to row numbers and saved to '{output_csv}'.")
