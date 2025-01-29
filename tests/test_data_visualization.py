
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_visualization import time_series_visualization,visualize_all_conditions, plot_brain_region_analysis
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

    def test_visualize_all_conditions():
    # Sample dataset for testing
        data = {
        'subject_identifier': ['group1', 'group1', 'group2', 'group2', 'group1', 'group2'],
        'condition': ['condition1', 'condition1', 'condition1', 'condition2', 'condition2', 'condition2'],
        'value': [1.2, 2.3, 1.4, 2.1, 0.9, 1.0]
        }
        combined_df = pd.DataFrame(data)

    # Patch plt.show() to prevent the plot from displaying during the test
        with patch('matplotlib.pyplot.show') as mock_show:
        # Call the function
         visualize_all_conditions(
            combined_df,
            value='value',
            condition_column='condition',
            subject_identifier='subject_identifier'
        )

        # Check if plt.show() was called, indicating that the plot was generated
        mock_show.assert_called_once()

    # Optionally: Check that the function didn't raise any exceptions
    # If no exceptions were raised, the test passes.

