import os
import serial
import csv
import argparse
import time

def main(com_port, filename, official):

    # Create the "csv" folder if it doesn't exist
    if not os.path.exists("csv/"):
        os.makedirs("csv/")
    if not os.path.exists("csv/official/"):
        os.makedirs("csv/offical/")
    if not os.path.exists("csv/unofficial/"):
        os.makedirs("csv/unofficial/")

    # Construct the full path for the CSV file in the appropriate folder
    csv_path = os.path.join("csv/", "official/" if official else "unofficial/", filename)

    print(f"Wait 2 seconds and then save data to '{csv_path}'")
    time.sleep(2)

    # Open the serial port
    ser = serial.Serial(com_port, 9600)

    # Open a CSV file for writing
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header row to the CSV file
        csv_writer.writerow(['ax', 'ay', 'az', 'gx', 'gy', 'gz'])

        # Continuously read and write data until the connection is closed
        while ser.is_open:
            try:
                # Read a line of data from the serial port
                line = ser.readline().decode('utf-8').strip()

                # Split the line into individual values
                values = line.split()

                # Check if the line has all the required values
                if len(values) == 6:
                    ax, ay, az, gx, gy, gz = values
                    csv_writer.writerow([ax, ay, az, gx, gy, gz])
                    print(f"Recorded: ax={ax}, ay={ay}, az={az}, gx={gx}, gy={gy}, gz={gz}")

            except KeyboardInterrupt:
                print("KeyboardInterrupt: Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    # Close the serial port
    ser.close()

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Read data from a serial port and save it to a CSV file")
    parser.add_argument('com_port', help="Name of the COM port")
    parser.add_argument('filename', help="Name of the CSV file to save data")
    parser.add_argument('--official', action='store_true', default=False, help="Save the CSV file to the 'official' folder")
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.com_port, args.filename, args.official)