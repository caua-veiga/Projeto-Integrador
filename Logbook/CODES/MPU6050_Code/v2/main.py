from machine import Pin, SoftI2C, lightsleep
import math
import mpu6050
from time import ticks_ms
import json

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32

mpu= mpu6050.accel(i2c)

def wrap(angle, limit):
    """
    Pushes angle to a set range
    """
    while angle > limit:
        angle -= 2*limit
    while angle < -limit:
        angle += 2*limit
    return angle

def calibrate():
    offsets = [0, 0, 0, 0, 0] # ax, ay, az, gx, gy
    count = 0
    total = 1000
    # Calculate average offset value
    while count < total:
        count += 1
        raw_measurements = mpu.get_values()
        measurements = list(unpack(raw_measurements))
        for i, offset in enumerate(offsets):
            offsets[i] = offsets[i] + (measurements[i] - offsets[i])/count
    offsets[2] = offsets[2] - 1.0 #
    return offsets


def unpack(values, offsets=None):
    """
    Unpacks output of register reader and normalizes the raw sensor input
    according to values given in datasheet for set register fullscale range
    """
    accel_x = values["AcX"] / 16384.0
    accel_y = values["AcY"] / 16384.0
    accel_z = values["AcZ"] / 16384.0
    gyro_x = values["GyX"] / 131.0
    gyro_y = values["GyY"] / 131.0
    if offsets != None:
        accel_x -= offsets[0]
        accel_y -= offsets[1]
        accel_z -= offsets[2]
        gyro_x -= offsets[3]
        gyro_y -= offsets[4]
    return accel_x, accel_y, accel_z, gyro_x, gyro_y

# Calibrate before using to determine sensor offset values
# Must position sensor on flat surface
offsets = calibrate()
with open('calibration_offsets.json', 'w') as file:
    json.dump(offsets, file) # Store calibration results (radians)

roll = 0
rad2deg = 180/math.pi
previousTime = ticks_ms()
sampling_interval = 10 # ms

while True:

    currentTime = ticks_ms()
    elapsedTime = currentTime - previousTime
    # set a samping rate
    if elapsedTime > sampling_interval:

        previousTime = currentTime

        raw_measurements = mpu.get_values() # read sensor data
        ax, ay, az, gx, gy = unpack(raw_measurements, offsets=offsets) # extract signals from dictionary


        # calculate inclination angle from accelerometer output
        accel_angle = math.atan(ay/math.sqrt(ax*ax + az*az))

        # apply complimentary filter to combine both sensors signal
        # note that we are only interested in the roll angle
        roll = 0.98*(roll + (gx * (elapsedTime/1000))) + 0.02*accel_angle*rad2deg


        # accel_angle = wrap(accel_angle, limit=180)
        # gyro_angle = wrap(gyro_angle, limit=180)

        toPrint = str(accel_angle*rad2deg) + "/"
        # toPrint += str(gyro_angle)  + "/"
        toPrint += str(roll)
        print(toPrint)





