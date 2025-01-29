import pandas as pd
import pytest
from src.data_analysis import compute_group_differences, map_sensors_to_regions, assign_brain_region, perform_t_tests, analyze_responses_by_condition_and_group
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
from io import StringIO
from unittest.mock import patch


# Sample test data for compute_group_differences
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "sensor_position": ["CP1", "CP2", "P3", "P4", "F7", "F8"],
        "subject_id": ["a", "a", "a", "c", "c", "c"],
        "value": [10.5, 8.2, 7.1, 6.0, 9.3, 8.8],
        "group": ["alcoholic", "alcoholic", "alcoholic", "control", "control", "control"],
    })


# Test compute_group_differences
def test_compute_group_differences(sample_data):
    result = compute_group_differences(
        combined_df=sample_data,
        value="value",
        subject_id="group",
        position="sensor_position",
        group1="alcoholic",
        group2="control",
    )
    # Validate output structure
    assert isinstance(result, pd.DataFrame)
    assert "difference" in result.columns
    # Validate sorted order
    assert result["difference"].is_monotonic_decreasing
    # Validate that rows match sensor positions
    assert set(result.index) == set(sample_data["sensor_position"].unique())


# Sample test data for map_sensors_to_regions
@pytest.fixture
def sample_sensor_data():
    return pd.DataFrame({
        "sensor_position": ["CP1", "P3", "F7", "Z9", "Unknown"],
        "value": [1.0, 2.0, 3.0, 4.0, 5.0],
    })


# Test map_sensors_to_regions
def test_map_sensors_to_regions(sample_sensor_data):
    result = map_sensors_to_regions(data=sample_sensor_data, sensor_column="sensor_position")
    # Validate output structure
    assert isinstance(result, pd.DataFrame)
    assert "region" in result.columns
    # Validate region assignments
    assert result.loc[result["sensor_position"] == "CP1", "region"].iloc[0] == "Sensory-Motor Cortex"
    assert result.loc[result["sensor_position"] == "P3", "region"].iloc[0] == "Parietal Lobe"
    assert result.loc[result["sensor_position"] == "F7", "region"].iloc[0] == "Frontal Lobe"
    # Validate dropping of unknown regions
    assert result["sensor_position"].isin(["Unknown"]).sum() == 0


# Test assign_brain_region separately
def test_assign_brain_region():
    assert assign_brain_region("CP1") == "Sensory-Motor Cortex"
    assert assign_brain_region("P3") == "Parietal Lobe"
    assert assign_brain_region("Z9") == "Unknown Region"
    assert assign_brain_region("Unknown") == "Unknown Region"


def test_perform_t_tests():
    # Sample dataset
    data = {
        'subject_id': ['group1', 'group1', 'group2', 'group2', 'group1', 'group2'],
        'position': ['Fz', 'Cz', 'Fz', 'Cz', 'Pz', 'Pz'],
        'value': [1.2, 2.3, 1.4, 2.1, 0.9, 1.0]
    }
    combined_df = pd.DataFrame(data)

    # Mock the `assign_brain_region` function to test specific behavior
    def mock_assign_brain_region(sensor):
        region_mapping = {
            'Fz': 'Frontal',
            'Cz': 'Central',
            'Pz': 'Parietal'
        }
        return region_mapping.get(sensor, 'Unknown Region')

    # Replacing the original `assign_brain_region` with the mock version
    with patch('data_analysis.assign_brain_region', side_effect=mock_assign_brain_region):
        
        # Capture the output using StringIO to test what the function prints
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Run the function
            perform_t_tests(
                combined_df,
                value='value',
                subject_id='subject_id',
                position='position',
                group1='group1',
                group2='group2',
                unknown_regions=['X', 'Y'],
                alpha=0.05
            )

            # Get the output printed by the function
            output = mock_stdout.getvalue()

            # Check the output for the expected result
            assert "Frontal: Fz" in output
            assert "Central: Cz" in output
            assert "Parietal: Pz" in output
            assert "No sensor positions showed statistically significant differences." not in output

            # Check if the correct regions are mentioned (just for illustration)
            assert "Frontal" in output
            assert "Central" in output
            assert "Parietal" in output


# Assuming the analyze_responses_by_condition_and_group function is already defined

def test_analyze_responses_by_condition_and_group():
    # Sample dataset for testing
    data = {
        'subject_identifier': ['group1', 'group1', 'group1', 'group2', 'group2', 'group2'],
        'condition': ['condition1', 'condition1', 'condition2', 'condition1', 'condition2', 'condition2'],
        'value': [1.2, 2.3, 1.4, 2.1, 0.9, 1.0]
        }
    combined_df = pd.DataFrame(data)

    # Call the function to analyze responses by condition and group
    result = analyze_responses_by_condition_and_group(
        combined_df,
        value='value',
        condition='condition',
        subject_identifier='subject_identifier'
        )

    # Manually compute the expected result for testing
    expected_result = pd.DataFrame({
        'condition': ['condition1', 'condition1', 'condition2', 'condition2'],
        'subject_identifier': ['group1', 'group2', 'group1', 'group2'],
        'mean': [1.75, 2.15, 1.4, 0.95],
        'std': [0.777817, 0.070711, 0.0, 0.0]
        })

    # Sort both the result and expected dataframe to ensure the comparison is correct (in case of row ordering differences)
    result_sorted = result.sort_values(by=['condition', 'subject_identifier']).reset_index(drop=True)
    expected_result_sorted = expected_result.sort_values(by=['condition', 'subject_identifier']).reset_index(drop=True)

    # Round the 'mean' values to avoid small floating point differences
    result_sorted['mean'] = result_sorted['mean'].round(2)
    expected_result_sorted['mean'] = expected_result_sorted['mean'].round(2)

    # Use assert_frame_equal with check_like=True to allow for column/row order differences
    pd.testing.assert_frame_equal(result_sorted, expected_result_sorted, check_like=True)

