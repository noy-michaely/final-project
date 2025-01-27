# tests/test_data_cleaning.py
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import unittest
from unittest.mock import patch
from src.data_cleaning import csv_combined, convert_numeric_val

class TestCsvCombined(unittest.TestCase):
    
    @patch("glob.glob")
    @patch("pandas.read_csv")
    def test_csv_combined(self, mock_read_csv, mock_glob):
        # Setup the mock for glob to return a list of CSV file paths
        mock_glob.return_value = ["file1.csv", "file2.csv"]
        
        # Setup the mock for pd.read_csv to return mock data
        mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        
        # Call the function
        combined_df = csv_combined("mock_directory")
        
        # Assert that pd.read_csv was called twice (once for each file)
        mock_read_csv.assert_called_with("file2.csv")
        
        # Assert that the combined DataFrame has the correct shape
        self.assertEqual(combined_df.shape, (2, 2))  # 2 files, 2 rows each

    def test_numeric_val(self):
        # Create a sample DataFrame
        df = pd.DataFrame({
            'column1': ['1', '2', 'three', '4.5', 'NaN', '6'],
            'column2': ['a', 'b', 'c', 'd', 'e', 'f']
        })

        # Apply the function
        convert_numeric_val('column1', df)

        # Check the results
        self.assertTrue(pd.api.types.is_numeric_dtype(df['column1']), "Column should be numeric.")
        self.assertEqual(df['column1'].isnull().sum(), 2, "Two non-convertible values should result in NaNs.")

        print("All tests passed for convert_numeric_val.")
