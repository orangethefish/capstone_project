# Running the IMU Capture and CSV Upload Scripts

To use these scripts, follow these steps:

# Getting Started

This project use the following packages:
`pip install os, time, csv, serial, requests, json, argparse`

# To run 

## IMU Capture Script

Flash the IMU with the `IMU_Capture.ino` script. This script will capture the IMU data and send it to the serial port.

## CSV Upload Script

Run the `to_csv.py` script. This script will read the serial port and write the data to a CSV file. The script will also upload the CSV file to the server.
The scipt takes 3 arguments: port, filename, and official (optional). port is the COM port of the connected devices, filename is the name of the CSV file, and official is a boolean value that determines if the data is official or not if official is true the data will be saved in csv/official and csv/unofficial otherwise. The default value for official is false.

Sample command to run the script with COM3, A.csv and official data:
`python to_csv.py COM6 A.csv --official`