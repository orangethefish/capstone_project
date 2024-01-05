import tensorflow as tf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Dropout, LSTM, Reshape


GESTURES = [
    "A"
]
labels = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]
NUM_GESTURES = len(GESTURES)
ONE_HOT_ENCODED_GESTURES = np.eye(NUM_GESTURES)

# NUM_OF_RECORDINGS  =

inputs = []

for gesture_index in range (NUM_GESTURES):
  gesture = GESTURES[gesture_index]
  print(f"Processing index {gesture_index} for gesture '{gesture}'.")
  output = ONE_HOT_ENCODED_GESTURES[gesture_index]
  for i in range(0, 11 ):
    filename = f"csv/unofficial/{gesture}/{gesture}_{i}.csv"
    print(f"Processing file: {filename}")
    df = pd.read_csv(filename)
    input = df.to_numpy().flatten()
    padded_sequence = pad_sequences([input], maxlen=540, dtype='float32', padding='post', truncating='post')
    inputs.append(padded_sequence[0])

inputs = np.array(inputs)
inputs_test = tf.convert_to_tensor(inputs, dtype=tf.float32)

# Load your trained model
model = tf.keras.models.load_model('result')
# Use the model to predict the inputs
predictions = model.predict(inputs_test)
#check if the prediction is label B
num_correct = 0
for prediction in predictions:
    if prediction[labels.index(GESTURES[0])] > 0.5:
        num_correct += 1

print("number of correct predictions:", num_correct)
print("total number of predictions:", len(predictions))

# print the predictions and the expected ouputs
print("predictions =\n", np.round(predictions, decimals=3))