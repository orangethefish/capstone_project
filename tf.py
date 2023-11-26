import tensorflow as tf

print(tf.__version__)


SEED = 2023
tf.random_set_seed(SEED)

GESTURES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L","M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V","W", "X", "Y", "Z"
]