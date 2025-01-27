
import matplotlib.pyplot as plt
import seaborn as sns

def time_series_visualization(combined_df, time,value,subject_identifier):
    sns.lineplot(data=combined_df, x=time, y=value, hue=subject_identifier)
    plt.title("EEG Response Over Time:")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Sensor Value (µV)")
    plt.show()


def sensors_differences_heatmap(combined_df, subject_identifier, position, value, group1, group2):
    # Group data by sensor position and subject identifier, then compute the mean sensor value difference
    group1_data = combined_df[combined_df[subject_identifier] == group1]
    group2_data = combined_df[combined_df[subject_identifier] == group2]
    
    group1_means = {}
    group2_means = {}
    for sensor_pos in group1_data[position].unique():
        group1_means[sensor_pos] = group1_data[group1_data[position] == sensor_pos][value].mean()

    # Calculate the mean sensor value for each sensor position for group2
    for sensor_pos in group2_data[position].unique():
        group2_means[sensor_pos] = group2_data[group2_data[position] == sensor_pos][value].mean()

    # Create a list of sensor positions
    sensor_positions = list(group1_means.keys())

    # Initialize a list to store the differences
    differences = []

    # Calculate the differences for each sensor position
    for pos in sensor_positions:
        diff = group1_means.get(pos, 0) - group2_means.get(pos, 0)
        differences.append(diff)
    
    # Create a 2D structure (list of lists) for heatmap
    # The first list will contain all the differences for a single row (since it's comparing two groups)
    heatmap_data = [differences]  # Creating a 2D list (1 row with the differences)

    # Plotting the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=False, cmap='coolwarm', center=0, cbar_kws={'label': 'Difference in Mean Sensor Value (µV)'},
                fmt=".2f", yticklabels=[f'Difference ({group1} vs {group2})'], xticklabels=sensor_positions,
                linewidths=0.5, linecolor='black')

    # Customize plot appearance
    plt.title(f"EEG Differences Between {group1} and {group2} by Sensor Position", fontsize=16)
    plt.xlabel("Sensor Position", fontsize=12)
    plt.ylabel(f"Difference in Mean {group1} vs {group2}", fontsize=12)
    plt.tight_layout()
    plt.show()

# Step 3: Visualization
def plot_brain_region_analysis(grouped_data, subject_identifier, value, title="Absolute Mean EEG Values by Brain Region and Group"):
    """
    Plot a bar chart for mean EEG values grouped by brain region and subject group.
    
    Args:
        grouped_data (pd.DataFrame): Grouped data (mean values by region and group).
        title (str): Title of the plot.
    """
    grouped_data = grouped_data.groupby(["region", subject_identifier])[value].mean().unstack()
    grouped_data = grouped_data.abs()
    grouped_data.plot(kind="bar", figsize=(10, 6), colormap="coolwarm")
    plt.title(title, fontsize=16)
    plt.xlabel("Brain Region", fontsize=12)
    plt.ylabel("Mean Value", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Group", fontsize=10)
    plt.tight_layout()
    plt.show()


