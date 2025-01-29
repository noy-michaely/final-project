
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_analysis import compute_group_differences

def time_series_visualization(combined_df, time,value,subject_identifier):
    sns.lineplot(data=combined_df, x=time, y=value, hue=subject_identifier)
    plt.title("EEG Response Over Time:")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Sensor Value (µV)")
    plt.show()


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


def visualize_all_conditions(combined_df, value, condition_column, subject_identifier):
    """
    Visualizes the response values for each condition, separated by group (e.g., alcoholic vs control),
    using both a box plot and bar plot.
    
    Args:
        combined_df (pd.DataFrame): The dataset to analyze.
        value (str): Column name for numerical values.
        condition_column (str): Column name for the conditions (e.g., "matching_condition").
        subject_identifier (str): Column name for the group (e.g., "subject_identifier").
    """
    plt.figure(figsize=(10, 6))
    condition_group_means = combined_df.groupby([condition_column, subject_identifier])[value].mean().reset_index()
    condition_group_means[value] = condition_group_means[value].abs()
    sns.barplot(x=condition_column, y=value, hue=subject_identifier, data=condition_group_means)
    plt.title("Mean Response by Condition and Group")
    plt.xlabel("Condition")
    plt.ylabel("Mean Response Value")

    plt.tight_layout()
    plt.show()



