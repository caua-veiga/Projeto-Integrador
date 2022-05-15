# Progress update, week 4

We have the MPU 6050 sensor and managed to access its registers. We can now measure with a three-axis accelerometer and a gyroscope. 

We implemented a routine to extract inclination angle from the sensor data, and to combine them using a complimentary filter. 

We have to check if the accelerometer data treatment is correct. The gyroscope was already verified.

We came across a problem when generating PWM with the ESP-32 over low frequencies. We required this in order to control the ESC, since it is controlled as a servomotor: 50 Hz PWM with negative duty cycle inbetween 5-10 % 

The workaround is to use the Nano Arduino board to generate PWM and control it through the ESP32. We need to set up this control flow.

We also realized that in order to treat data from sensors, we need to be able to transfer it to our computer. We can do this via cable and it'd probably be easier, but since the idea is to think about the project as an introduction to drone control, it makes more sense to do it via wi-fi. This way we avoid physical connections which would be prohibited had we been dealing with a real drone.

We are still waiting for the support + joint to be ordered by our professor. 

