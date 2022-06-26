# Week 5

## 16/05 

The sensor code is completed.

We have sucessfully retrieved the raw data from its registers and converted it to usable data resorting to its datasheet.

We combined both the gyroscope and accelerometer data by the means of a complimentary filter in order to get the final angle measurement. 

We also implemented an autocalibration function in order to correct sensor offsets. 
   
- [x] Sensor programming 

## 18/05

We updated the sensor code.

We now request measurements in a given sampling rate by accessing the hardware's timer.

We also estimate the angular velocity to later use as a second input to our RL algorithm. 

We flashed an updated firmware that corrected the PWD bug.

We are now able to generate 50 Hz PWM as required by the ESC. Therefore, we no longer need a second board to control the motors.  

- [x] Fix firmware bug to generate required PWM 
 
## 20/08

We are now ready to implement the system, since the support was made available to us. 

We successfully controlled the motors with the ESC32. They are now placed with the correct orientation on the support.

We needed to convert the PWM signal from 3.3V logic to 5V. We dimensioned a non-inverting amplifier to do so.

We also learnt basic soldering to join pins to new boards and to connect wires.  We also learnt how to apply rubber coating to exposed wire junctions.

We researched into Wi-Fi communication and we are now able to attempt hosting a HTTP server in our ESP32 to send data to a live feed. 

We also further researched PID implementation and we are now ready to do so.  We shall implement an incremental algorithm, with integral action limitting (to avoid windup) and low-pass filtering of derivative action (to avoid noise amplification). We also shall design the experiment required for PID constant tuning through the Ziegler-Nichols method. 

- [x] Physical setup
- [x] Motor control with ESP32
- [x] Wi-Fi implementation planning
- [x] PID implementation planning
 
