from machine import Pin, SoftI2C, lightsleep
import math
import mpu6050
from time import ticks_ms
import time
import json
from pid import PID
import socket
from motor import Motor

def do_connect():
    '''
    Input must be a tuple: (essid, password)
    '''
    import network

    essid =  'iPhone Caua' #'iPhone Caua' #'UPTEC' #'Galaxy A32 5G1A70'
    password = 'caualex12' #'caualex12' #'UPTECNET'  #'yfee4537'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...',end='\n')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    #print('network config:', wlan.ifconfig())

#do_connect()

i2c = SoftI2C(scl=Pin(22), sda=Pin(21)) # Initializing the I2C method for ESP32

mpu= mpu6050.accel(i2c)


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
offsets = [0.01475194, -0.02073169, -0.1112247, 9.591637, 1.257359]
print("Done calibrating sensor",end='\n')

def calibrate_ESC(motor1, motor2):
    print('ENTREI CALIB')
    time.sleep_ms(2000)
    print('Writing minimum output',end='\n')
    motor1.setPWM(0)
    motor2.setPWM(0)
    time.sleep_ms(2500)
    print('Writing maximum output',end='\n')
    motor1.setPWM(1)
    motor2.setPWM(1)
    print('Esc is Calibrated!\nNow you can enter any value between 0 and 1')
    time.sleep_ms(550)
    motor1.setPWM(0)
    motor2.setPWM(0)

motorLeft = Motor(15)
motorRight = Motor(25)
print("Calibrating motors...")
calibrate_ESC(motorLeft, motorRight)
print("Done calibrating motors")

# Operating on IPv4 addressing scheme
#serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind and listen
#serverSocket.bind(("172.20.10.5",80)) #192.168.203.53 #172.20.10.5
#serverSocket.listen()
# Wait for client connection
#connected = False
#while not connected:
    # Accept connections
#    (clientConnected, clientAddress) = serverSocket.accept()
#    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
#    if clientConnected:
#        connected = True




# Main loop
def main_loop():
    # Initialize variables
    roll = 0
    rad2deg = 180/math.pi
    totalTime = ticks_ms()
    previousTime = ticks_ms()
    sampling_interval = 10 # ms
    # Intialize controller
    controller = PID(Kp=0.15, Kd=0.1, Ki=0.01)
    # Choose setpoint
    controller.uc = 25

    while True:
        currentTime = ticks_ms()
        elapsedTime = currentTime - previousTime
        # Set a samping rate
        if elapsedTime > sampling_interval:
            previousTime = currentTime

            raw_measurements = mpu.get_values() # Read sensor data
            ax, ay, az, gx, gy = unpack(raw_measurements, offsets=offsets) # Extract signals from dictionary

            # Calculate inclination angle from accelerometer output
            accel_angle = math.atan(ay/math.sqrt(ax*ax + az*az))

            dt = (elapsedTime/1000)
            # Apply complimentary filter to combine both signals
            roll = 0.98*(roll + (gx * dt)) + 0.02*accel_angle*rad2deg

            #print(f'Angle: {roll}')
            controller.write(roll, dt)
            controller_output = controller.read()
            print(f"P={controller.P:.3f} D={controller.D:.3f} I={controller.I:.3f} U={controller_output:.3f} A={roll:.2f}")

            # Write controller output to motors
            motorLeft.writePWM(0.5*controller_output)
            motorRight.writePWM(-0.5*controller_output)

            # Note: the program won't advance until the client sends the acknowledgement data
            # This may affect the chosen sampling rate
            #dataFromClient = clientConnected.recv(1024)
            # Send some data back to the client
            #data = {'Angle': roll, 'Time': totalTime/1000}
            #data = json.dumps(data)
            #clientConnected.send(data.encode("utf-8"))

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated")
finally:
    motorLeft.deinit()
    motorRight.deinit()

