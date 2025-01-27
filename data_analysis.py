def compute_group_differences(combined_df, value, subject_id, position, group1, group2):
    """
    Computes mean differences in sensor values between two groups for each sensor position.

    Args:
        df (DataFrame): The dataset to analyze.
        value (str): Column name for numerical values (
        subject_id (str): Column name for group/category 
        position (str): Column name for sensor positions 
        group1 (str): Label for the first group 
        group2 (str): Label for the second group 

    Returns:
        DataFrame: A DataFrame showing mean values for each group, differences, and sorted by difference.
    """
    # Compute mean sensor values for each group at each sensor position
    grouped = (
        combined_df.groupby([position, subject_id])[value]
        .mean()
        .unstack(fill_value=0)
         # Creates separate columns for group1 and group2
    )

    # Add a column for the absolute difference
    grouped["difference"] = abs(grouped[group1] - grouped[group2])
    # Sort by the largest difference
    sorted_diff = grouped.sort_values(by="difference", ascending=False)
    print("Top 10 Sensor Positions with Most Pronounced Differences:")
    print(sorted_diff.head(10))

    return sorted_diff

def map_sensors_to_regions(data, sensor_column):
    """
    Map EEG sensors to brain regions and add a 'region' column to the DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing sensor data.
        sensor_column (str): The name of the column with sensor identifiers.

    Returns:
        pd.DataFrame: The updated DataFrame with a new 'region' column.
    """
    data["region"] = data[sensor_column].apply(assign_brain_region)
    data = data.dropna(subset=["region"])
    data = data[data["region"] != "Unknown Region"]
    return data


# Define a list of tuples (prefix, region)
region_mapping = [
    ("CP", "Sensory-Motor Cortex"),
    ("P", "Parietal Lobe"),
    ("PO", "Parietal-Occipital Lobe"),
    ("C", "Central Sulcus"),
    ("T", "Temporal Lobe"),
    ("TP", "Temporal-Parietal Lobe"),
    ("F", "Frontal Lobe"),
    ("FC", "Motor Cortex"),
    ("FT", "Frontal-Temporal Lobe"),
]

# Function to assign brain regions
def assign_brain_region(sensor_name):
    return next(
        (region for prefix, region in region_mapping if sensor_name.startswith(prefix)),
        "Unknown Region",  # Default value
    )

# Apply the mapping function


