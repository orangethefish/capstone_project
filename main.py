import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

pi = math.pi
g_value = 9.80665
RAD_TO_DEG = 57.2957795131
COMPLE_ALPHA = 0.05
fileLength = 0
time_interval = 0.01


# Low-pass filter
class RCFilter:
    def __init__(self, cutoffFreqHz, sampleTimeS):
        # Compute equivalent 'RC' constant from cut-off frequency
        RC = 1.0 / (pi * 2 * cutoffFreqHz)

        # Pre-compute filter coefficients for the first-order low-pass filter
        self.coeff = [sampleTimeS / (sampleTimeS + RC), RC / (sampleTimeS + RC)]

        # Clear output buffer
        self.out = [0.0, 0.0]

    def update(self, inp):
        # Shift output samples
        self.out[1] = self.out[0]

        # Compute new output sample
        self.out[0] = self.coeff[0] * inp + self.coeff[1] * self.out[1]

        # Return filtered sample
        return self.out[0]


# Load the CSV file
input_file = "sensor_data.csv"  # Replace with the actual file path
with open(input_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Initialize lists to store data
    accel_x_data = []
    accel_y_data = []
    accel_z_data = []
    gyro_x_data = []
    gyro_y_data = []
    gyro_z_data = []

    # Loop through each line in the CSV file
    for data in csv_reader:
        accel_x_data.append(float(data['Accelerometer X (g)']))
        accel_y_data.append(float(data['Accelerometer Y (g)']))
        accel_z_data.append(float(data['Accelerometer Z (g)']))
        gyro_x_data.append(float(data['Gyroscope X (rad/s)']))
        gyro_y_data.append(float(data['Gyroscope Y (rad/s)']))
        gyro_z_data.append(float(data['Gyroscope Z (rad/s)']))
        fileLength += 1

# Initialise low-pass filters
lpfAcc = [RCFilter(5.0, 0.01) for _ in range(3)]
lpfGyr = [RCFilter(25.0, 0.01) for _ in range(3)]

# Initialize lists to store filter
filtered_acc_x = []
filtered_acc_y = []
filtered_acc_z = []
filtered_gyr_x = []
filtered_gyr_y = []
filtered_gyr_z = []

# Filter accelerometer data and gyroscope data
for i in range(fileLength):
    filtered_acc_x.append(lpfAcc[0].update(accel_x_data[i]))
    filtered_acc_y.append(lpfAcc[1].update(accel_y_data[i]))
    filtered_acc_z.append(lpfAcc[2].update(accel_z_data[i]))
    filtered_gyr_x.append(lpfGyr[0].update(gyro_x_data[i]))
    filtered_gyr_y.append(lpfGyr[1].update(gyro_y_data[i]))
    filtered_gyr_z.append(lpfGyr[2].update(gyro_z_data[i]))

# Initialize lists of roll and pitch of accelerometer, gyroscope and the complementary roll and pitch
roll_acc = []
pitch_acc = []
roll_gyr = []
pitch_gyr = []
roll = [0, ]
pitch = [0, ]


for i in range(fileLength):
    # Calculate pitch and roll angles using accelerometer data
    roll_acc.append(np.arctan2(filtered_acc_y[i], filtered_acc_z[i]))
    pitch_acc.append(np.arcsin(filtered_acc_x[i] / g_value))

    roll_gyr.append(filtered_gyr_x[i] + np.tan(pitch[i]) *
                    (np.sin(roll[i]) * filtered_gyr_y[i] + np.cos(roll[i]) * filtered_gyr_z[i]))
    pitch_gyr.append(np.cos(roll[i]) * filtered_gyr_y[i] - np.sin(roll[i]) * filtered_gyr_z[i])

    roll.append((COMPLE_ALPHA * roll_acc[i] + (1.0 - COMPLE_ALPHA) * (roll[i] + 0.01 * roll_gyr[i])))
    pitch.append((COMPLE_ALPHA * pitch_acc[i] + (1.0 - COMPLE_ALPHA) * (pitch[i] + 0.01 * pitch_gyr[i])))


result_data = pd.DataFrame({'Roll (degrees)': roll, 'Pitch (degrees)': pitch})


# Write the pitch and roll data to a new CSV file
output_file = 'pitch_and_roll_data.csv'  # Replace with your desired output file path
if not os.path.exists(output_file):
    result_data.to_csv(output_file, index=False)

# Create subplots for roll and pitch
plt.figure(figsize=(12, 6))
time_data = [i * time_interval for i in range(fileLength + 1)]
plt.plot(time_data, roll, label='Roll')
plt.plot(time_data, pitch, label='Pitch')
plt.xlabel('Time')
plt.ylabel('Angle (rad)')
plt.legend()
plt.title('Roll and Pitch Over Time (Assuming Constant Time Interval)')
plt.grid(True)

plt.show()
