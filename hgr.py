import tensorflow as tf
import seaborn as sns
import numpy as np
import pandas as pd
import keras
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Dropout, LSTM, Reshape, Conv2D, MaxPooling2D, Conv1D, MaxPooling1D, Flatten, GlobalAveragePooling1D
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers.legacy import Adam
print(tf.__version__)


SEED = 2023
tf.random.set_seed(SEED)

GESTURES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z", "idle"
]

NUM_GESTURES = len(GESTURES)
ONE_HOT_ENCODED_GESTURES = np.eye(NUM_GESTURES)

NUM_OF_RECORDINGS  = 300

inputs = []
outputs = []


for gesture_index in range (NUM_GESTURES):
  gesture = GESTURES[gesture_index]
#   print(f"Processing index {gesture_index} for gesture '{gesture}'.")
  output = ONE_HOT_ENCODED_GESTURES[gesture_index]
  for i in range(NUM_OF_RECORDINGS):
    filename = f"csv/official/{gesture}/{gesture}_{i}.csv"
    # print(f"Processing file: {filename}")
    df = pd.read_csv(filename)
    input = df.to_numpy().flatten()
    padded_sequence = pad_sequences([input], maxlen=540, dtype='float32', padding='post', truncating='post')
    inputs.append(padded_sequence[0])
    outputs.append(output)

inputs = np.array(inputs)
outputs = np.array(outputs)

print('input shape: ', inputs.shape)
print(inputs.shape[0], 'training samples')
print('output shape: ', outputs.shape)

# print("Data set parsing and preparation complete.")

"""#Randomize and split the input and output pairs for training"""

num_inputs = len(inputs)
randomize = np.arange(num_inputs)
np.random.shuffle(randomize)

# Swap the consecutive indexes (0, 1, 2, etc) with the randomized indexes
inputs = inputs[randomize]
outputs = outputs[randomize]

# Split the recordings (group of samples) into three sets: training, testing and validation
TRAIN_SPLIT = int(0.6 * num_inputs)
TEST_SPLIT = int(0.2 * num_inputs + TRAIN_SPLIT)

inputs_train, inputs_test, inputs_validate = np.split(inputs, [TRAIN_SPLIT, TEST_SPLIT])
outputs_train, outputs_test, outputs_validate = np.split(outputs, [TRAIN_SPLIT, TEST_SPLIT])


inputs_validate = tf.convert_to_tensor(inputs_validate, dtype=tf.float32)
outputs_validate = tf.convert_to_tensor(outputs_validate, dtype=tf.float32)

inputs_train = tf.convert_to_tensor(inputs_train, dtype=tf.float32)
outputs_train = tf.convert_to_tensor(outputs_train, dtype=tf.float32)

inputs_test = tf.convert_to_tensor(inputs_test, dtype=tf.float32)
outputs_test = tf.convert_to_tensor(outputs_test, dtype=tf.float32)

# print("Data set randomization and splitting complete.")

# print("Input Data Types:", inputs_train.dtype, outputs_train.dtype)
# print("Input Shapes:", inputs_train.shape, outputs_train.shape)
# print("Input Validate Types:", inputs_validate.dtype, outputs_validate.dtype)
# print("Input Validate Shapes:", inputs_validate.shape, outputs_validate.shape)

"""##Build and Train the model"""


# train_dataset = tf.data.Dataset.from_tensor_slices((inputs_train, outputs_train))
# LEARNING_RATE = 0.0005
# opt = Adam(learning_rate=LEARNING_RATE, beta_1=0.9, beta_2=0.999)
# # build the model and train it
# model = tf.keras.Sequential()
# #add LSTM layer
# # model.add(LSTM(100, input_shape=(300,1), return_sequences=True))
# model.add(Dense(100,kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4),
#     bias_regularizer=regularizers.L2(1e-4),
#     activity_regularizer=regularizers.L2(1e-5), activation='relu')) # relu is used for performance
# model.add(Dropout(0.5))
#
# model.add(Dense(NUM_GESTURES, activation='softmax')) # softmax is used, because we only expect one gesture to occur per input
# model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['category_accuracy'])
# history = model.fit(inputs_train, outputs_train, epochs=200, batch_size=64, validation_data=(inputs_validate, outputs_validate) )
# model.summary()
# 1D CNN neural network
model_m = tf.keras.Sequential()
model_m.add(Reshape((90, 6), input_shape=(540,)))
model_m.add(Conv1D(100, 10, activation='relu', input_shape=(90, 6)))
model_m.add(Conv1D(100, 10, activation='relu'))
model_m.add(MaxPooling1D(3))
model_m.add(Dropout(0.3))
model_m.add(Conv1D(160, 10, activation='relu'))
model_m.add(Conv1D(160, 10, activation='relu'))
model_m.add(GlobalAveragePooling1D())
model_m.add(Dropout(0.5))
model_m.add(Dense(27, activation='softmax'))
print(model_m.summary())
# keras.utils.plot_model(model_m, show_shapes=True)

callbacks_list = [
    keras.callbacks.ModelCheckpoint(
        filepath='model_CNN/best_model.{epoch:02d}-{val_loss:.2f}.h5',
        monitor='val_loss', save_best_only=True),
    keras.callbacks.EarlyStopping(monitor='accuracy', patience=5)
]

model_m.compile(loss='categorical_crossentropy',
                optimizer='adam', metrics=['accuracy'])

# Hyper-parameters
BATCH_SIZE = 400
EPOCHS = 50

# Enable validation to use ModelCheckpoint and EarlyStopping callbacks.
history = model_m.fit(inputs_train,
                      outputs_train,
                      batch_size=BATCH_SIZE,
                      epochs=EPOCHS,
                      callbacks=callbacks_list,
                      validation_split=0.2,
                      verbose=1)

plt.figure(figsize=(6, 4))
plt.plot(history.history['accuracy'], 'r', label='Accuracy of training data')
plt.plot(history.history['val_accuracy'], 'b', label='Accuracy of validation data')
plt.plot(history.history['loss'], 'r--', label='Loss of training data')
plt.plot(history.history['val_loss'], 'b--', label='Loss of validation data')
plt.title('Model Accuracy and Loss')
plt.ylabel('Accuracy and Loss')
plt.xlabel('Training Epoch')
plt.ylim(0)
plt.legend()
plt.show()

# use the model to predict the test inputs
predictions = model_m.predict(inputs_test)

# print the predictions and the expected ouputs
print("predictions =\n", np.round(predictions, decimals=3))
print("actual =\n", outputs_test)

# print the correct predictions out of all predictions
num_correct = 0
for i in range(len(predictions)):
    if np.argmax(predictions[i]) == np.argmax(outputs_test[i]):
        num_correct += 1

print("number of correct predictions:", num_correct)
print("total number of predictions:", len(predictions))


# Save the entire model to a single file with a timestamp in the name
model_m.save('result')


# Plot the predictions along with to the test data
