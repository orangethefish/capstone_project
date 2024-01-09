import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Reshape

def create_dataset(X, y, time_steps=1, step=1):
    Xs, ys = [], []
    for i in range(0, len(X) - time_steps, step):
        v = X.iloc[i:(i + time_steps)].values
        labels = y.iloc[i: i + time_steps]
        Xs.append(v)        
        ys.append(np.unique(labels)[0])
    return np.array(Xs), np.array(ys).reshape(-1, 1)

TIME_STEPS = 70
STEP = 20
GESTURES = [
    "A"
]
labels = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]
NUM_GESTURES = len(GESTURES)
NUM_OF_RECORDINGS = 400
g = 9.81
column_mapping = {
    'column_0': 'ax',
    'column_1': 'ay',
    'column_2': 'az',
    'column_3': 'gx',
    'column_4': 'gy',
    'column_5': 'gz',
}
#training have shape (num_of_samples, 70, 6)
#reshape a sample file to (70, 6)
ONE_HOT_ENCODED_GESTURES = np.eye(NUM_GESTURES)
inputs = []
for label in GESTURES:
    # for i in range(99,100):
        df_train = pd.read_csv(f"csv/official/{label}/{label}_0.csv")
        df_train = df_train.rename(columns=column_mapping)
        df_train = df_train.iloc[9:85]
        inputs = df_train
inputs = inputs.values.reshape(-1, 70, 6)
inputs = tf.convert_to_tensor(inputs, dtype=tf.float32)
model = tf.keras.models.load_model('lstm')
predictions = model.predict(inputs)
#check if the prediction is label B
num_correct = 0
for prediction in predictions:
    if prediction[labels.index(GESTURES[0])] > 0.5:
        num_correct += 1

print("number of correct predictions:", num_correct)
print("total number of predictions:", len(predictions))

# print the predictions and the expected ouputs
print("predictions =\n", np.round(predictions, decimals=3))