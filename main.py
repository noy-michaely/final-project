import src.data_cleaning as data_cleaning
import src.data_analysis as data_analysis
import src.data_visualization as data_visualization 
# import pandas as pd

def main():
    
    # 1. File Directory Path 
    directory_path = "C:/Users/User/.cache/kagglehub/datasets/nnair25/Alcoholics/versions/1" 

    # 2. Load and Combine Data
    combined_df = data_cleaning.csv_combined(directory_path)
    
    # 3. Data Cleaning
    data_cleaning.convert_numeric_val('sensor value', combined_df)  # Convert 'sensor value' to numeric
    
    combined_df.to_csv("cleaned_data.csv", index=False)

    # Parameters for analysis
    value = "sensor value"         # Column with numerical data
    subject_identifier = "subject identifier"  # Column identifying groups (Alcoholic vs Control)
    position = "sensor position"  # Column with sensor positions
    group1 = "a"                      # Alcoholic group
    group2 = "c"                      # Control group
    data_analysis.compute_group_differences(combined_df, value, subject_identifier, position, group1, group2)
    sensor_df = data_analysis.map_sensors_to_regions(combined_df, sensor_column="sensor position")

    # 5. Visualization
    data_visualization.sensors_differences_heatmap(combined_df, subject_identifier, position ,value,group1,group2)
    data_visualization.plot_brain_region_analysis( sensor_df,
        value='sensor value',
        subject_identifier='subject identifier')
    # Time series visualization
    data_visualization.time_series_visualization(
        combined_df=combined_df,
        time='time',
        value='sensor value',
        subject_identifier='subject identifier'
    )
    
    # Differences in sensor responses
    
if __name__=='__main__':
    main()
