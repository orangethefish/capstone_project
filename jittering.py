import numpy as np
import pandas as pd
import os

# Define the jittering function
def jittering(time_series, noise_factor=0.01):
    """
    Apply jittering to a given time series by adding random noise.

    Parameters:
    - time_series: numpy array, the original time series
    - noise_factor: float, the scaling factor for the random noise (default is 0.01)

    Returns:
    - jittered_series: numpy array, the time series after jittering
    """

    # Generate random noise with the same length as the time series
    random_noise = np.random.normal(0, noise_factor, len(time_series))

    # Add the random noise to the original time series
    jittered_series = time_series + random_noise

    return jittered_series

# Specify the label
GESTURES = [
    "S", "T", "U", "V","W", "X", "Y", "Z"
]
for label in GESTURES:
    # Directory containing the original CSV files
    input_directory = f'csv/official/{label}/'

    # Directory to save the new CSV files with jittered data
    output_directory = f'csv/official/{label}/'

    # Ensure the output directory exists, create if necessary
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through each original CSV file
    for i in range(100):
        input_filename = f'{label}_{i}.csv'
        output_filename = f'{label}_{i+200}.csv'

        # Read the original CSV file
        original_data = pd.read_csv(os.path.join(input_directory, input_filename))

        # Extract the time series data from each column
        original_time_series_columns = [original_data[col].values for col in original_data.columns]

        # Apply jittering to each column
        noise_factor = 0.01
        jittered_time_series_columns = [jittering(column, noise_factor) for column in original_time_series_columns]

        # Combine the jittered columns into a new DataFrame
        jittered_data = pd.DataFrame({f'column_{i}': column for i, column in enumerate(jittered_time_series_columns)})

        # Save the jittered data to a new CSV file
        jittered_data.to_csv(os.path.join(output_directory, output_filename), index=False)
