import numpy as np
import pandas as pd
import os

# Assuming you have a time_warping function defined as before
def time_warping(time_series, factor):
    """
    Apply time warping to a given time series.

    Parameters:
    - time_series: numpy array, the original time series
    - factor: float, the warping factor (1.0 for no warp, <1.0 for compression, >1.0 for stretching)

    Returns:
    - warped_series: numpy array, the time series after time warping
    """

    # Create a new time axis after warping
    warped_time_axis = np.arange(0, len(time_series), factor)

    # Interpolate the time series data to the new time axis
    warped_series = np.interp(warped_time_axis, np.arange(len(time_series)), time_series)

    return warped_series
GESTURES = [
    "S", "T", "U", "V","W", "X", "Y", "Z"
]
for label in GESTURES:
    # Directory containing the original CSV files
    input_directory = f'csv/official/{label}/'

    # Directory to save the new CSV files with time-warped data
    output_directory = f'csv/official/{label}/'

    # Ensure the output directory exists, create if necessary
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Iterate through each original CSV file
    for i in range(100):
        input_filename = f'{label}_{i}.csv'
        output_filename = f'{label}_{i+100}.csv'

        # Read the original CSV file
        original_data = pd.read_csv(os.path.join(input_directory, input_filename))

        # Extract the time series data (assuming it's in a column named 'value')
        original_time_series_columns = [original_data[col].values for col in original_data.columns]

        # Apply time warping with a factor, e.g., 1.5 for stretching
        warping_factor = 1.5
        warped_time_series_columns = [time_warping(column, warping_factor) for column in original_time_series_columns]

        # Combine the time-warped columns into a new DataFrame
        warped_data = pd.DataFrame({f'column_{i}': column for i, column in enumerate(warped_time_series_columns)})
        warped_data.to_csv(os.path.join(output_directory, output_filename), index=False)
