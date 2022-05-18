# Week 5 Roadmap

## 16/05

The sensor code is completed. We have sucessfully retrieved the raw data from its registers and converted it to usable data resorting to its datasheet. We combined both the gyroscope and accelerometer data by the means of a complimentary filter in order to get the final angle measurement. We also implemented an autocalibration function in order to correct sensor offsets.

- [x] Sensor programming

## 18/05

We updated the sensor code. We now request measurements in a given sampling rate by accessing the hardware's timer. We also estimate the angular velocity to later use as a second input to our RL algorithm.

We flashed an updated firmware that corrected the PWD bug. We are now able to generate 50 Hz PWM as required by the ESC. Therefore, we no longer need a second board to control the motors. 

- [x] Fix firmware bug to generate required PWM 
