from machine import Pin, SoftI2C, sleep
import math
import mpu6050
from time import ticks_ms
import json

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32

mpu= mpu6050.accel(i2c)

def unpack(values):
    accel_x = values["AcX"]
    accel_y = values["AcY"]
    accel_z = values["AcZ"]
    gyro_x = values["GyX"]
    gyro_y = values["GyY"]
    return accel_x, accel_y, accel_z, gyro_x, gyro_y

gyro_angle = 0

while True:

    start = ticks_ms()
    values = mpu.get_values() # read sensor data
    now = ticks_ms()

    ax, ay, az, gx, gy = unpack(values) # extract signals from dictionary

    # calculate inclination angle
    # from accelerometer output
    accel_angle = math.atan((ay/16384.0)/(math.sqrt((ax/16384.0)**2))
                  + (az/16384.0)**2)

    # normalize gyroscope output
    # according to datasheet
    gx /= 131.0
    gy /= 131.0

    # integrate gyroscope output
    gyro_angle += gx * (now - start)/1000

    # apply complimentary filter to combine
    # both sensors signal
    angle = 0.98*gyro_angle + 0.02*accel_angle
    rad2deg = 180 / math.pi
    toPrint = str(accel_angle*rad2deg) + "/"
              + str(gyro_angle*rad2deg)  + "/"
              + str(angle*rad2deg)
    print(toPrint)
    sleep(20)

