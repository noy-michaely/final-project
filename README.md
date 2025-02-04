# EEG Analysis Project

## Overview
This project analyzes EEG data to investigate differences in brain activity between alcoholic and control subjects. The analysis pipeline includes data cleaning, statistical analysis, and visualization of EEG signals across different brain regions.

The project is implemented in Python and follows a modular structure with separate components for data cleaning, analysis, and visualization. 

---
## Objectives, Assumptions and Hypothesis
The objective of this project is to identify significant trends in EEG sensor data and evaluate how specific brain regions and sensors differ between two groups.

This project assumes the data being used isn't corrupted, and contains .csv files of standard EEG data (e.g - sensor position, sensor value, conditions, etc...) of two groups.

Our hypothesis with regards to our own data (comparing a group of alcoholics and a control group) is that major differences will be found between activities within brain regions that are associated with inebriation and/or decision making. A hypothesis which would prove true in our case.


---

## Features
- **Data Cleaning**: Combines multiple CSV files, removes duplicates, handles missing values, and converts numerical values.
- **Data Analysis**: Maps sensors to brain regions, computes group differences, and performs statistical tests.
- **Visualizations**: Generates time-series plots, bar charts, and condition-based response comparisons.
- **Testing**: Includes unit tests to ensure correctness of data processing and analysis functions.

---

## File Structure
```
final_project/
├── src/
│   ├── data_cleaning.py         # Data preprocessing and cleaning logic
│   ├── data_analysis.py         # Functions for analyzing EEG data
│   ├── data_visualization.py    # Visualization functions for EEG data
│
├── tests/
│   ├── test_data_cleaning.py    # Unit tests for data cleaning
│   ├── test_data_analysis.py    # Unit tests for data analysis
│   ├── test_data_visualization.py # Unit tests for data visualization
│
├── README.md                    # Project documentation
├── finalproject.toml          # Required dependancies
└── main.py                      # Entry point for the pipeline
```

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/noy-michaely/final-project.git
   cd eeg-analysis
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the Pipeline**:
   - Execute the main script to clean, analyze, and visualize the data:
     ```bash
     python main.py
     ```

2. **Run Tests**:
   - To ensure all components are working as expected, run the test suite:
     ```bash
     python -m pytest
     ```

3. **View Results**:
   - Visualizations will be saved in the code.

---

## Key Analysis
### Research Questions
1. **How does the EEG response evolve over time during the trial for alcoholic versus control subjects?**
2. **Which specific brain regions show the most pronounced differences in EEG responses between alcoholic and control groups?**

### Methods
- **Sensor Mapping**: EEG sensors are assigned to specific brain regions based on predefined mappings.
- **Group Comparison**: Computes mean differences in EEG signals between alcoholic and control subjects.
- **Statistical Testing**: Performs independent t-tests to identify significant differences in brain activity.
- **Visualization**: Generates bar plots, time-series graphs, and heatmaps to illustrate key findings.

---

## Requirements
The following Python libraries are required:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy`
- `pytest`
- `unittest`
- `glob`

---

## Example Visualizations
1. **EEG Response Over Time**: Line plots showing sensor activity changes across time for different groups.
2. **Brain Region Analysis**: Bar charts comparing absolute mean EEG values across brain regions.
3. **Condition-Based Response Comparison**: Bar plot visualizing EEG activity under different experimental conditions.

---

## Bibliography
dataset: https://www.kaggle.com/datasets/nnair25/Alcoholics/data
original dataset research: https://archive.ics.uci.edu/dataset/121/eeg+database
data for sensor position mapping: https://www.researchgate.net/publication/322322733_EEG_signal_clustering_for_motor_and_imaginary_motor_tasks_on_hands_and_feet 