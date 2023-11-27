import os
import serial
import csv
import argparse
import time

def main(com_port, label_name, official):

    # Create the "csv" folder if it doesn't exist
    if not os.path.exists("csv/"):
        os.makedirs("csv/")
    if not os.path.exists("csv/official/"):
        os.makedirs("csv/official/")
    if not os.path.exists("csv/unofficial/"):
        os.makedirs("csv/unofficial/")
    
    # Generate a unique filename based on the label name and the current time
    recording = 0
    #stops if recording > 50
    filename = f"{label_name}_{recording}.csv"

    while True:
        # Construct the full path for the CSV file in the appropriate folder
        if official:
            folder_path = "csv/official/"
        else:
            folder_path = "csv/unofficial/"
        if not os.path.exists(f"{folder_path}/{label_name}"):
            os.makedirs(f"{folder_path}/{label_name}")
        csv_path = os.path.join(folder_path, filename)

        # Print the filename and start recording
        print(f"Wait 2 seconds before recording data to '{csv_path}' for 2 seconds...")
        for i in range(2,0,-1):
            print(i)
            time.sleep(1)
        # Open the serial port
        ser = serial.Serial(com_port, 9600)

        # Open a CSV file for writing
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row to the CSV file
            csv_writer.writerow(['ax', 'ay', 'az', 'gx', 'gy', 'gz'])

            # Start the timer
            start_time = time.time()

            # Continuously read and write data until the connection is closed or the timer expires
            while ser.is_open and (time.time() - start_time) < 2:
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
                    os.remove(csv_path)  # Delete the recorded file
                    break
                except Exception as e:
                    print(f"Error: {e}")

        # Close the serial port
        ser.close()

        save_recording = input("Save this recording? (Press enter to continue or press any other key to delete) ")
        if save_recording != '':
            os.remove(csv_path)  # Delete the recorded file
            continue
        else:
            recording += 1
        if recording >= 100:
            break
        # Check if recording should continue
        # if input("Continue recording? (Press enter to continue or press any other key to exit) " ) != '':
        #     break
        # Increment the file number for the next recording
        filename = f"{label_name}_{recording}.csv"

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Read data from a serial port and save it to a CSV file")
    parser.add_argument('com_port', help="Name of the COM port")
    parser.add_argument('label_name', help="Label name for the CSV file")
    parser.add_argument('--official', action='store_true', default=False, help="Save the CSV file to the 'official' folder")
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.com_port, args.label_name, args.official)
