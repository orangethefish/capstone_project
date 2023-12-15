from flask import Flask, jsonify, request
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model('test')

@app.route('/capstone/api/predictions', methods=['POST'])
def get_predictions():
    try:
        # Assuming the frontend sends JSON data in the request body
        body = request.get_json()
        # data = body['readings']

        # Extract and process data for prediction
        inputs_for_test = process_input_data(body)

        # Apply PCA to get the matrix Z
        z_matrix = apply_pca(inputs_for_test)

        # Convert to tensorflow data
        inputs_tf = get_input_data(z_matrix)

        # Use the model to predict the inputs
        predictions = model.predict(inputs_tf)

        # Convert predictions to a list for easier JSON serialization
        predictions_list = predictions.tolist()

        # Return predictions as JSON
        return jsonify({'predictions': predictions_list})

    except Exception as e:
        return jsonify({'error': str(e)})


def process_input_data(data):
    # Get the column names from the first object in the array
    column_names = list(data[0].keys())

    # Extract values from each object using dynamic column names
    X = np.array([[item[column] for column in column_names] for item in data])

    return X


def apply_pca(data):
    g_value = 9.80665

    n, M = data.shape #row and column of original matrix

    L = 3
    #Number of elements to keep

    XX = data.copy()

    # Add 4g and divide the first 3 columns by 8g
    data[:, :3] = (data[:, :3] + 4 * g_value) /  (8 * g_value)

    # Add 2000 and divide the last 3 columns by 4000
    data[:, 3:] = (data[:, 3:] + 2000) / 4000

    m = np.mean(data, axis=0) #mean of X

    #Subtract the mean from each value of X so that the data does not vary too much when calculating
    for i in range(n):
        data[i, :] = data[i, :] - m

    #Covariance matrix
    Q = np.dot(np.transpose(data.copy()), data) / (n-1)

    #Getting Eigen values and Eigen vectors
    Eigenval, Eigenvec = np.linalg.eig(Q)


    Eval = np.real(Eigenval)

    # Sort the Eigen values in decreasing order, the bigger the value the more important it represents
    Evalsorted = np.sort(Eval)[::-1]

    Index = np.argsort(Eval)[::-1]

    # Sort the Eigen vectors depend on its values
    Evecsorted = Eigenvec[:, Index]


    Ppca = Evecsorted[:, :L] #Basis principal-component vectors

    #Final data
    Z = np.dot(data, Ppca) #Reducing the dimensionality

    print('Original Data:')
    print(XX)
    print('Principal Component Basis Vectors:')
    print(Ppca)
    print('Transformed Data:')
    print(Z)

    return Z



def get_input_data(data):

    # Flatten the entire 2D array
    flattened_array = data.flatten()

    # Pad the flattened array to a length of 320
    padded_sequence = pad_sequences([flattened_array], maxlen=300, dtype='float32', padding='post', truncating='post')

    # Convert the padded sequence to a TensorFlow tensor
    inputs_test = tf.convert_to_tensor(padded_sequence, dtype=tf.float32)

    return inputs_test


if __name__ == '__main__':
    app.run(port=8035, debug=True)
