import src.data_cleaning as data_cleaning
import src.data_analysis as data_analysis
import src.data_visualization as data_visualization 

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
    unknown_regions = ['x','y','nd']
    condition = "matching condition"
    data_analysis.perform_t_tests(combined_df, value, subject_identifier, position, group1, group2, unknown_regions)
    data_analysis.compute_group_differences(combined_df, value, subject_identifier, position, group1, group2)
    sensor_df = data_analysis.map_sensors_to_regions(combined_df, sensor_column="sensor position")
    condition_group_stats = data_analysis.analyze_responses_by_condition_and_group(
    combined_df,
    value,         # Column containing the numerical response values
    condition,  # Column for conditions ("S1 obj", "S2 matching", etc.)
    subject_identifier  # Column that separates alcoholic ('a') and control ('c')
    )

    print(condition_group_stats)    

    # 5. Visualization
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
    data_visualization.visualize_all_conditions(combined_df, value, condition,subject_identifier)
    
if __name__=='__main__':
    main()
