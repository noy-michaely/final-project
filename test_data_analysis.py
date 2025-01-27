import pandas as pd
import pytest
from src.data_analysis import compute_group_differences, map_sensors_to_regions, assign_brain_region
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend

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
