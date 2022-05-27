import time
from machine import Pin, PWM
import uasyncio


class Motor():

    def __init__(self,PIN):
        self.pwm = PWM(Pin(PIN)) # Defining the GPIO Pin that will output our PWM signal
        self.pwm.freq(50) # The frequency of our PWM will always be 50Hz


    def writePWM(self, dut):
        new_dut = self.pwm.duty() + dut
        new_dut = 0 if new_dut < 0 else new_dut
        #new_dut = 1. if new_dut > 1 else new_dut
        new_dut = 0.15 if new_dut > 0.15 else new_dut
        x = (new_dut+1)/20
        duty = int(x*1023)
        
        self.pwm.duty(duty)


    def calibrateESC(self):
        time.sleep_ms(1500)
        print('Writing minimum output',end='\n')
        self.writePWM(int(1/20 * 1023))
        time.sleep_ms(2000)
        print('Writing maximum output',end='\n')
        self.writePWM(int(2/20 * 1023))
        print('Esc is Calibrated!\nNow you can enter any value between 0 and 1')
        time.sleep_ms(350)
        self.writePWM(int(1/20 * 1023))
