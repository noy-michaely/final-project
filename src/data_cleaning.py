import pandas as pd
import glob
import os
 #write definition for each function 

def csv_combined(directory_path):
    # finding all CSV files in the directory and its subdirectories
    csv_files = glob.glob(os.path.join(directory_path, "**", "*.csv"), recursive=True)

    # Initializig an empty list to hold DataFrames
    data_frames = []

    # Looping through each CSV file and read it into a DataFrame
    for file in csv_files:
        print(f"Reading file: {file}")  # Check which file is being processed
        try:
            df = pd.read_csv(file)
            if df.empty:
                print(f"Warning: {file} is empty.")
            else:
                data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    # Checking if any DataFrames were added
    if len(data_frames) == 0:
        print("No data frames to concatenate.")
    else:
        # Combining all the DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.drop_duplicates(inplace=True)
    combined_df.dropna(inplace=True)
    return combined_df


def convert_numeric_val(columname,combined_df):
    combined_df[columname] = pd.to_numeric(combined_df[columname], errors='coerce')
    

    