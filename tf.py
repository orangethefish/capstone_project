import tensorflow as tf
import numpy as np
import pandas as pd
import re
import os

print(tf.__version__)


SEED = 2023
tf.random.set_seed(SEED)

# GESTURES = [
#     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
#     "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
#     "U", "V","W", "X", "Y", "Z", "idle"
# ]

GESTURES = [
    "A", "B", "C", "idle"
]
NUM_GESTURES = len(GESTURES)
ONE_HOT_ENCODED_GESTURES = np.eye(NUM_GESTURES)

NUM_OF_RECORDINGS  = 100

inputs = []
outputs = []


for gesture_index in range (NUM_GESTURES):
  gesture = GESTURES[gesture_index]
  print(f"Processing index {gesture_index} for gesture '{gesture}'.")  
  output = ONE_HOT_ENCODED_GESTURES[gesture_index]
  for i in range(NUM_OF_RECORDINGS):
    filename = f"content/drive/MyDrive/dataset/{gesture}_{i}_pca.csv"
    print(f"Processing file: {filename}")
    df = pd.read_csv(filename)
    input = df.to_numpy().flatten()
    inputs.append(input)
    outputs.append(output)

