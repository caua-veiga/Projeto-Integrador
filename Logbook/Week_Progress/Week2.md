# Plan to the class

1. Control the motor with the arduino

2. Test the MPU6050 IMU sensor and properly identify how it operates (what are it's outputs and how to work with it)

3. Ask the professor to manufacture the joint.

# Work Before Class 

1. Continue to gather useful references and indentify/test virtual environments to train the RL Agent

2. Design the joint to be manufactured (if we can find the mesurements online, otherwise we have to mesure it and design during class)

3. Install IDE and Python dependence 'firmata' - https://realpython.com/arduino-python/

## Note

There are two options for controlling the Arduino board with Python. 

The pyfirmata package implements the Firmata protocol to communicate with the board through Python. However, it is compatible only with Python 2.7, 3.3 and 3.4 - https://pypi.org/project/pyFirmata/

The other option is to use MicroPython through the OpenMV Editor (not sure if Mu Editor cuts it for Arduino). However, there are few boards supporting MicroPython and we must check if one is available to us - https://docs.arduino.cc/learn/programming/arduino-and-python#compatible-boards. Namely, the compatible boards are:

- Nano 33 BLE
- Nano 33 BLE Sense
- Nano RP2040 Connect
- Portenta H7

# Work During Class

## 1 - Control the motor with Arduino

As we have seen last week the ESC properly converts a voltage input to motor speed control linearly. 

A guide on how it works and how to control: https://www.youtube.com/watch?v=uOQk8SJso6Q

![Arduino_ESC_Diagram](Arduino_ESC_Diagram.png)

### 1.. - ESC Calibration
Code to calibrate the ESC - 

http://electronoobs.com/eng_robotica_tut5_1_code1.php

### 1.1 - Setup at fixed voltage

In the referenced video it is used a potentiometer so that the voltage can be changed manually resulting in a manual controll of the output thrust of the motor. 

As a first step I suggest we take a more conservative and simple approach, to get more confident with the material. To do so, instead of using a potentiometer we should go with a fixed voltage and see how it works.

### 1.2 - Potentiometer

Although our final goal is not to controll the motor manually but rather with no human input, it could be of great value adding a potentiometer to easily make some tests at different voltages input and collect some datapoints on the motor performance, since we don't have a very in-deep datasheet about it.

### 1.3 - Automatically control the voltage output

Going fowards our final goal we should define how to properlly control the voltage input without a (manual) potentiometer. (no ideal yet, should search for references...)

## 2 - Test the MPU6050 IMU sensor and properly identify how it operates

*Note* that gyroscope and accelerometer sensor data of MPU6050 module consists of 16-bit raw data in 2’s complement form. 
The complete documentation, including the datasheet and register map can be seen at - https://www.electronicwings.com/sensors-modules/mpu6050-gyroscope-accelerometer-temperature-sensor-module

### 2.1 - Read the data from the accelerometer
'''

Copied from the source code http://electronoobs.com/eng_robotica_tut6_1_code1.php#google_vignette

This is the full PID Code used at https://www.youtube.com/watch?v=AN3yxIBAxTA&t=787s 

''' 

We know that the slave adress fro this IMU is 0x68 in hexadecimal. For that in the RequestFrom and the begin funcitons we gave to put this value.

     Wire.beginTransmission(0x68);
     Wire.write(0x3B); //Ask for the 0x3B register- correspond to AcX
     Wire.endTransmission(false);
     Wire.requestFrom(0x68,6,true);  

We have asked for the 0x3B register. The IMU will send a brust of register. The amount of register to read is specify in the requestFrom functioon- In this case we resquest 6 registers. Each value of acceleration is made out of two 8-bits registers, low values and high values. For that we shift to the left the high values register (<<) and make and or (|) operation to add the low values.

     Acc_rawX=Wire.read()<<8|Wire.read(); //each value needs two registres
     Acc_rawY=Wire.read()<<8|Wire.read();
     Acc_rawZ=Wire.read()<<8|Wire.read();

This is the part where you need to calculate the angles using Euler equations
    
  Now, to obtain the values of acceleration in "g" units we first have to divide the raw  values that we have just read by 16384.0 because that is the value that the MPU6050 datasheet gives us. Next we have to calculate the radian to degree value by dividing 180º by the PI number which is 3.141592654 and store this value in the rad_to_deg variable. In order to not have to calculate this value in each loop we have done that just once before the setup void. 

Now we can apply the Euler formula. The atan will calculate the arctangent. The pow(a,b) will elevate the a value to the b power. And finnaly sqrt function will calculate the rooth square.

    /*---X---*/

     Acceleration_angle[0] = atan((Acc_rawY/16384.0)/sqrt(pow((Acc_rawX/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;

     /*---Y---*/
     Acceleration_angle[1] = atan(-1*(Acc_rawX/16384.0)/sqrt(pow((Acc_rawY/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;


### 2.2 - Read the data from the gyroscope

Now we read the Gyro data in the same way as the Acc data. The adress for the gyro data starts at 0x43. We can see this adresses if we look at the register map of the MPU6050. In this case we request just 4 values. W don¡t want the gyro for  the Z axis (YAW).

     Wire.beginTransmission(0x68);
     Wire.write(0x43); //Gyro data first adress
     Wire.endTransmission(false);
     Wire.requestFrom(0x68,4,true); //Just 4 registers

     Gyr_rawX=Wire.read()<<8|Wire.read(); //Once again we shif and sum
     Gyr_rawY=Wire.read()<<8|Wire.read();

Now in order to obtain the gyro data in degrees/seconds we have to divide first the raw value by 131 because that's the value that the datasheet gives us.

     /*---X---*/
     Gyro_angle[0] = Gyr_rawX/131.0; 
     
     /*---Y---*/
     Gyro_angle[1] = Gyr_rawY/131.0;


Then in order to obtain degrees we have to multiply the degree/seconds value by the elapsedTime. Finnaly we can apply the final filter where we add the acceleration part that afects the angles and ofcourse multiply by 0.98.

     /*---X axis angle---*/
     Total_angle[0] = 0.98 *(Total_angle[0] + Gyro_angle[0]*elapsedTime) + 0.02*Acceleration_angle[0];
     
     /*---Y axis angle---*/
     Total_angle[1] = 0.98 *(Total_angle[1] + Gyro_angle[1]*elapsedTime) + 0.02*Acceleration_angle[1];
   
Now we have our angles in degree and values from -10º0 to 100º aprox

     Serial.println(Total_angle[1]);
    
## 3 - Joint Manufacture

Sugestion (after we take the mesures I can design a final version o CAD):

![Scketch Joint](Scketch_Joint.png)
