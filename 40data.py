import serial
import random
import time

# Open serial port
ser = serial.Serial('/dev/ttys005', 9600)  # Replace 'COM1' with the appropriate port name

while True:
    # Start string
    ser.write(b"START,")

    for i in range(40):
        random_value = random.randint(0, 99)  # Generate a random value between 0 and 99

        ser.write(str(random_value).encode())  # Send the random value over serial

        if i < 39:
            ser.write(b",")  # Add a comma to separate values, except for the last value

    # Stop string
    ser.write(b",STOP\r\n")

    time.sleep(0.1)  # Wait for 10 milliseconds before sending the next set of random value