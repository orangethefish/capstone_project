import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Reshape
from sklearn.preprocessing import RobustScaler

GESTURES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]
label = "S"
column_mapping = {
    'column_0': 'ax',
    'column_1': 'ay',
    'column_2': 'az',
    'column_3': 'gx',
    'column_4': 'gy',
    'column_5': 'gz',
}

g= 9.81
#from csv/official/A_1.csv import to df
model = tf.keras.models.load_model('lstm')
correct = 0
for i in range(201,300):
    file_name = f'./csv/official/{label}/{label}_{i}.csv'   
    print(f"Reading file {file_name}")
    df = pd.read_csv(file_name)
    df = df.rename(columns=column_mapping)
    df['ax'] = (df['ax'] + 4*g) / (8*g)
    df['ay'] = (df['ay'] + 4*g) / (8*g)
    df['az'] = (df['az'] + 4*g) / (8*g)
    df['gx'] = (df['gx'] + 2000) / 4000
    df['gy'] = (df['gy'] + 2000) / 4000
    df['gz'] = (df['gz'] + 2000) / 4000
    df = df.iloc[15:85].astype('float').to_numpy()
    reshaped = df.reshape(1,70,6)
    print(df.shape)

    prediction = model.predict(reshaped)
    if GESTURES[np.argmax(prediction)]==label:
        correct += 1
print(correct)