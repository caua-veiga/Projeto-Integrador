from machine import Pin, SoftI2C, lightsleep
import math
import mpu6050
from time import ticks_ms
import time
import json
from pid import PID
import socket
from Calibrate_Motor import Motor

def do_connect():
    '''
    Input must be a tuple: (essid, password)
    '''
    import network

    essid =  'Galaxy A32 5G1A70' #'iPhone Caua' #'UPTEC' #'Galaxy A32 5G1A70'
    password = 'yfee4537' #'caualex12' #'UPTECNET'  #'yfee4537'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()


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

controller = PID(Kp=0.05, Td=0.5, Ti=10.)

def calibrateESC(motor1, motor2):
        time.sleep_ms(2000)
        print('Writing minimum output',end='\n')
        motor1.writePWM(int(1/20 * 1023))
        motor2.writePWM(int(1/20 * 1023))
        time.sleep_ms(2500)
        print('Writing maximum output',end='\n')
        motor1.writePWM(int(2/20 * 1023))
        motor2.writePWM(int(2/20 * 1023))
        print('Esc is Calibrated!\nNow you can enter any value between 0 and 1')
        time.sleep_ms(350)
        motor1.writePWM(int(1/20 * 1023))
        motor2.writePWM(int(1/20 * 1023))


motorLeft = Motor(15)
motorRight = Motor(25)
print("Calibrating left motor...")
#motorLeft.calibrateESC()
print("Calibrating right motor...")
#motorRight.calibrateESC()

calibrateESC(motorLeft,motorRight)
print("Finished calibrating motors...")

# operating on IPv4 addressing scheme

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind and listen
serverSocket.bind(("192.168.203.53",80)) #192.168.203.53 #172.20.10.5
serverSocket.listen()

connected = False

while True:

    try:
        while not connected:
            # Accept connections
            (clientConnected, clientAddress) = serverSocket.accept()
            print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))

            if clientConnected:
                connected = True

        currentTime = ticks_ms()
        elapsedTime = currentTime - previousTime
        # set a samping rate
        if elapsedTime > sampling_interval:

            previousTime = currentTime

            raw_measurements = mpu.get_values() # read sensor data
            ax, ay, az, gx, gy = unpack(raw_measurements, offsets=offsets) # extract signals from dictionary


            # calculate inclination angle from accelerometer output
            accel_angle = math.atan(ay/math.sqrt(ax*ax + az*az))


            dt = (elapsedTime/1000)
            # apply complimentary filter to combine both sensors signal
            # note that we are only interested in the roll angle
            roll = 0.98*(roll + (gx * dt)) + 0.02*accel_angle*rad2deg

            #print(f'Angle: {roll}')
            controller.write(roll, dt)
            controller_output = controller.read()
            print(f"P={controller.P:.3f}", f"{controller.D:.3f}", f"{controller.I:.3f}", f"{controller_output}:.3f")

            # Write controller output to motors
            motorLeft.writePWM(0.5*controller_output)
            motorRight.writePWM(-0.5*controller_output)

            dataFromClient = clientConnected.recv(1024)
            #print(dataFromClient.decode())

            # Send some data back to the client
            data = {'Angle': roll, 'Time': dt}
            data = json.dumps(data)

            clientConnected.send(data.encode("utf-8"))

    except KeyboardInterrupt:
            print("Program terminated")
            motorLeft.deinit()
            motorRight.deinit()
            break



