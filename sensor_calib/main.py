from machine import Pin, I2C, sleep
import math
import mpu6050
from time import ticks_ms

i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for

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
    values = mpu.get_values()
    now = ticks_ms()

    ax, ay, az, gx, gy = unpack(values)
    #print(ax, ay, az)
    accel_angle = math.atan((ay/16384.0)/(math.sqrt((ax/16384.0)**2))
                  + (az/16384.0)**2)

    gx /= 131.0
    gy /= 131.0

    gyro_angle += gx * (now - start)/1000

    # complimentary filter
    angle = 0.98*gyro_angle + 0.02*accel_angle

    print(angle * 180 / math.pi)
    sleep(10)
