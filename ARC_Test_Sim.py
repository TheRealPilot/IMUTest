# David Limpus Summer 2023 - Streaming sim data to Beaglbone
# This file streams simulated data to the beaglebone 
# to test the functionality of the beaglebone's driver

# ***************** IMPORTS *****************
import serial
import csv
import time

def send_data(ser, data):
    # Convert the data to a formatted string
    data_str = ','.join(str(value) for value in data)
    data_str = f"${data_str}*XX\r\n"  # Add the IMU message format

    # Send the data to the BeagleBone through UART
    ser.write(data_str.encode())

# Replace '/path/to/flight_data.csv' with the actual path to the flight data CSV file
flight_data_file = '/path/to/flight_data.csv'

# Identify the beaglebon port, and replace '/dev/ttyUSB0' with the actual serial port connected to the BeagleBone
serial_port = '/dev/ttyUSB0'

# Connect to the BeagleBone through UART
ser = serial.Serial(serial_port, 115200, timeout=0.1)

# Read flight data from the CSV file and emulate the datastream
with open(flight_data_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row if present in the CSV file

    for row in reader:
        yaw, pitch, roll, magX, magY, magZ, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, temp, pressure, time_ns = map(float, row)

        # Create a list containing the flight data for this row
        flight_data = [yaw, pitch, roll, magX, magY, magZ, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, temp, pressure, time_ns]

        # Send the data to the BeagleBone to emulate the IMU datastream
        send_data(ser, flight_data)

        # Adjust the delay based on the time difference between data points in IMU CSV file
        # 37.5 Hz = 0.0267 s
        time.sleep(0.0267)  

# Close the serial connection
ser.close()