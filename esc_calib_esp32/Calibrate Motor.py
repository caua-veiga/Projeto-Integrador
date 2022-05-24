import time
from machine import Pin, PWM
import uasyncio


class Calibrate(PIN):

    def __init__(self,PIN):
        self.pwm = PWM(Pin(PIN)) # Defining the GPIO Pin that will output our PWM signal
        self.pwm.freq(50) # The frequency of our PWM will always be 50Hz


    def Cpwm(self,dut):
        self.pwm.duty(dut)

    def CalEsc():
        time.sleep_ms(1500)
        print('Writing minimum output',end='\n')
        Cpwm(int(1/20 * 1023))
        time.sleep_ms(2000)
        print('Writing maximum output',end='\n')
        Cpwm(int(2/20 * 1023))
        print('Esc is Calibrated!\nNow you can enter any value between 0 and 1')
        time.sleep_ms(350)
        Cpwm(int(1/20 * 1023))

    def getPWM(self):
        return self.pwm