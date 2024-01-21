import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Reshape
# from tensorflow.keras.preprocessing.sequence import pad_sequences

GESTURES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]
column_mapping = {
    'column_0': 'ax',
    'column_1': 'ay',
    'column_2': 'az',
    'column_3': 'gx',
    'column_4': 'gy',
    'column_5': 'gz',
}
labels = ["A","Z"]
g= 9.81
#from csv/official/A_1.csv import to df
model = tf.keras.models.load_model('lstm')
for label in labels:
    correct = 0
    for i in range(0,10):
        file_name = f'./csv/unofficial/{label}/{label}_{i}.csv'   
        # print(f"Reading file {file_name}")
        df = pd.read_csv(file_name)
        df = df.rename(columns=column_mapping)
        df['ax'] = (df['ax'] + 4*g) / (8*g)
        df['ay'] = (df['ay'] + 4*g) / (8*g)
        df['az'] = (df['az'] + 4*g) / (8*g)
        df['gx'] = (df['gx'] + 2000) / 4000
        df['gy'] = (df['gy'] + 2000) / 4000
        df['gz'] = (df['gz'] + 2000) / 4000
        zeros_to_add = 85 - len(df)
        if zeros_to_add > 0:
            zeros_df = pd.DataFrame(0, index=np.arange(zeros_to_add), columns=df.columns)
            df = df.append(zeros_df, ignore_index=True)
        df = df.iloc[15:85].astype('float').to_numpy()
        reshaped = df.reshape(1,70,6)
        prediction = model.predict(reshaped)
        if GESTURES[np.argmax(prediction)]==label:
            correct += 1
    print(f"Accuracy for {label}: {correct}%")