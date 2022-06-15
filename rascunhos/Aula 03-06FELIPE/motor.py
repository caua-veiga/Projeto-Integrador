import time
from machine import Pin, PWM
import uasyncio


class Motor():

    def __init__(self,PIN):
        self.pwm = PWM(Pin(PIN)) # Defining the GPIO Pin that will output our PWM signal
        self.pwm.freq(50) # The frequency of our PWM will always be 50Hz


    def writePWM(self, inc):
        # Use only with the PID
        # This is meant to update the current duty value with an increment
        min_duty_allowed = 0.
        max_duty_allowed = 0.5
        new_duty = self.pwm.duty() + inc
        new_duty = 0 if new_duty < min_duty_allowed else new_duty
        new_duty = max_duty_allowed if new_duty > max_duty_allowed else new_duty
        x = (new_duty + 1)/20
        self.pwm.duty(int(x*1023))

    def setPWM(self, duty):
        # Use with calibration
        # This is meant to set a new absolute duty value
        if duty > 1:
            duty = 1
        x = (duty + 1)/20
        self.pwm.duty(int(x*1023))

    def deinit(self):
        self.pwm.deinit()
