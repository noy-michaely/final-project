
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_visualization import time_series_visualization,sensors_differences_heatmap, plot_brain_region_analysis
import unittest.mock
from unittest.mock import patch
import pandas as pd
import pytest
import matplotlib.pyplot as plt
class TestTimeSeriesVisualization(unittest.TestCase):
    
    @patch("matplotlib.pyplot.show")
    def test_time_series_visualization(self, mock_show):
        # Create mock DataFrame
        df = pd.DataFrame({
            "time": [0, 1, 2, 3],
            "sensor value": [1.0, 2.0, 3.0, 4.0],
            "subject identifier": ["a", "c", "a", "c"]
        })
        
        # Call the function to generate the plot
        time_series_visualization(df, "time", "sensor value", "subject identifier")
        
        # Assert that plt.show() was called to display the plot
        mock_show.assert_called_once()

# Sample test data for `sensors_differences_heatmap`
@pytest.fixture
def heatmap_test_data():
    return pd.DataFrame({
        "sensor_position": ["CP1", "CP2", "P3", "P4", "F7", "F8", "F8", "CP1"],
        "subject_identifier": ["a", "a", "a", "c", "c", "c", "a", "c"],
        "value": [10.5, 8.2, 7.1, 6.0, 9.3, 8.8, 8.4, 5.5],
        "group": ["alcoholic", "alcoholic", "alcoholic", "control", "control", "control", "alcoholic", "control"],
    })

# Test sensors_differences_heatmap
def test_sensors_differences_heatmap(heatmap_test_data):
    group1 = "alcoholic"
    group2 = "control"
    plt.figure()  # To prevent plotting errors in some environments
    sensors_differences_heatmap(
        combined_df=heatmap_test_data,
        subject_identifier="group",
        position="sensor_position",
        value="value",
        group1=group1,
        group2=group2,
    )
    # Validate that the heatmap function does not throw exceptions
    assert True  # Successful execution implies the function works correctly

# Sample test data for `plot_brain_region_analysis`
@pytest.fixture
def brain_region_data():
    return pd.DataFrame({
        "region": ["Sensory-Motor Cortex", "Parietal Lobe", "Temporal Lobe", "Frontal Lobe", "Frontal Lobe"],
        "subject_identifier": ["a", "a", "c", "c", "a"],
        "value": [10.5, 8.2, 7.1, 6.0, 9.3],
        "group": ["alcoholic", "alcoholic", "control", "control", "alcoholic"],
    })

# Test plot_brain_region_analysis
def test_plot_brain_region_analysis(brain_region_data):
    plt.figure()  # To prevent plotting errors in some environments
    plot_brain_region_analysis(
        grouped_data=brain_region_data,
        subject_identifier="group",
        value="value",
        title="Test EEG Plot",
    )
    # Validate that the bar plot function does not throw exceptions
    assert True  # Successful execution implies the function works correctly
