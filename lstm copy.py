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


labels = [ "A", "S","Z"]

#from csv/official/A_1.csv import to df
model = tf.keras.models.load_model('lstm')
for label in labels:
    correct = 0
    for i in range(0,10):
        file_name = f'./csv/unofficial/{label}/PCA/{label}_{i}_pca.csv'   
        # print(f"Reading file {file_name}")
        df = pd.read_csv(file_name)
        zeros_to_add = 85 - len(df)
        if zeros_to_add > 0:
            zeros_df = pd.DataFrame(0, index=np.arange(zeros_to_add), columns=df.columns)
            # df = df.append(zeros_df, ignore_index=True)
            df = pd.concat([df, zeros_df], ignore_index=True)
        df = df.iloc[15:85].astype('float').to_numpy()
        reshaped = df.reshape(1,70,3)
        prediction = model.predict(reshaped)
        if GESTURES[np.argmax(prediction)]==label:
            correct += 1
    print(f"Accuracy for {label}: {correct}%")