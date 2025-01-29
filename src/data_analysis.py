from scipy.stats import ttest_ind

# Define a list of tuples (prefix, region)
region_mapping = [
    ("CP", "Sensory-Motor Cortex"),
    ("P", "Parietal Lobe"),
    ("PO", "Parietal-Occipital Lobe"),
    ("C", "Central Sulcus"),
    ("T", "Temporal Lobe"),
    ("TP", "Temporal-Parietal Lobe"),
    ("F", "Frontal Lobe"),
    ("O", "Occipital Lobe"),
    ("FC", "Motor Cortex"),
    ("FT", "Frontal-Temporal Lobe"),
]
# Function to assign brain regions
def assign_brain_region(sensor_name):
    """
    Assigns a brain region based on the sensor name using predefined mappings.
    This version handles conflicts between short and long prefixes like 'P' and 'PO'.

    Args:
        sensor_name (str): The name of the EEG sensor.

    Returns:
        str: The corresponding brain region or 'Unknown Region' if not found.
    """
  
    # Special case for 'F' and 'AF' mapping to 'Frontal Lobe'
    if sensor_name.startswith('F') or sensor_name.startswith('AF'):
        return "Frontal Lobe"
    
    # Prioritize longer prefixes (e.g., 'PO', 'TP') first to avoid conflicts with shorter prefixes
    if sensor_name.startswith('PO'):
        return "Parietal-Occipital Lobe"
    if sensor_name.startswith('TP'):
        return "Temporal-Parietal Lobe"
    if sensor_name.startswith('FT'):
        return "Frontal-Temporal Lobe"
    if sensor_name.startswith('CP'):
        return "Sensory-Motor Cortex"
    if sensor_name.startswith('FC'):
        return "Motor Cortex"

    # Regular mapping based on the first two characters
    return next(
        (region for prefix, region in region_mapping if sensor_name.startswith(prefix)),
        "Unknown Region",  # Default value if not found
    )

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

def compute_group_differences(combined_df, value, subject_id, position, group1, group2):
    """
    Computes mean differences in sensor values between two groups for each sensor position.

    Args:
        combined_df (DataFrame): The dataset to analyze.
        value (str): Column name for numerical values.
        subject_id (str): Column name for group/category.
        position (str): Column name for sensor positions.
        group1 (str): Label for the first group.
        group2 (str): Label for the second group.

    Returns:
        DataFrame: A DataFrame showing mean values for each group, differences, and sorted by difference.
    """
    
    # Compute mean sensor values for each group at each sensor position
    grouped = combined_df.groupby([position, subject_id])[value].mean().unstack(fill_value=0)

    # Add a column for the absolute difference
    grouped["difference"] = abs(grouped[group1] - grouped[group2])
    
    # Sort by the largest difference
    sorted_diff = grouped.sort_values(by="difference", ascending=False)

    return sorted_diff


def perform_t_tests(combined_df, value, subject_id, position, group1, group2, unknown_regions, alpha=0.05):
    """
    Performs independent t-tests for each sensor position and prints only those with statistically significant differences,
    excluding sensors in the unknown_regions list. Groups the significant sensors by brain region.

    Args:
        combined_df (DataFrame): The dataset containing EEG data.
        value (str): Column name for numerical values.
        subject_id (str): Column name for group/category.
        position (str): Column name for sensor positions.
        group1 (str): Label for the first group.
        group2 (str): Label for the second group.
        unknown_regions (list): List of sensor positions to exclude from the t-tests.
        alpha (float, optional): Significance level for hypothesis testing (default is 0.05).

    Prints:
        Brain regions with significant sensors, formatted as: 
        "Region name: sensor1, sensor2, sensor3"
    """
    significant_sensors_by_region = {}

    for sensor in combined_df[position].unique():
        # Skip sensors listed in unknown_regions or invalid sensors like 'X', 'Y'
        if sensor in unknown_regions or assign_brain_region(sensor) == "Unknown Region":
            continue

        group1_values = combined_df[(combined_df[subject_id] == group1) & (combined_df[position] == sensor)][value]
        group2_values = combined_df[(combined_df[subject_id] == group2) & (combined_df[position] == sensor)][value]

        # Perform independent t-test
        t_stat, p_val = ttest_ind(group1_values, group2_values, equal_var=False, nan_policy='omit')

        # Check if significant
        if p_val < alpha:
            # Get the corresponding brain region for the sensor
            region = assign_brain_region(sensor)
            
            # Add the sensor to the corresponding region in the dictionary
            if region not in significant_sensors_by_region:
                significant_sensors_by_region[region] = []
            significant_sensors_by_region[region].append(sensor)

    # Print results by region
    if significant_sensors_by_region:
        print(f"The following regions have shown a significant difference (p < {alpha}):")
        for region, sensors in significant_sensors_by_region.items():
            print(f"{region}: {', '.join(sensors)}")
    else:
        print("No sensor positions showed statistically significant differences.")
    
def analyze_responses_by_condition_and_group(combined_df, value, condition, subject_identifier):
    """
    Analyzes the responses for each condition and group (e.g., alcoholic vs control) and computes statistics (mean, std) for each.

    Args:
        combined_df (pd.DataFrame): The dataset to analyze.
        value (str): Column name for numerical values.
        condition_column (str): Column name for the conditions (e.g., "matching_condition").
        group_column (str): Column name for the group (e.g., "subject_identifier").
    
    Returns:
        pd.DataFrame: A DataFrame showing the mean and standard deviation for each condition and group.
    """
    # Group by both condition and group, then calculate mean and std for each combination
    condition_group_stats = combined_df.groupby([condition, subject_identifier])[value].agg(['mean', 'std']).reset_index()

    return condition_group_stats





