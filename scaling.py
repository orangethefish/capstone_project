import pandas as pd
import random
GESTURES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]
for label in GESTURES:
    for i in range(100):
        input_file = f"csv/official/{label}/{label}_{i}.csv"
        output_file = f"csv/official/{label}/{label}_{i+300}.csv"

        # Load the input dataset
        df = pd.read_csv(input_file)

        # Perform scaling with a random float from 0.1 to 2
        scaled_df = df * random.uniform(2, 5)

        # Save the scaled dataset to the output file
        scaled_df.to_csv(output_file, index=False)
