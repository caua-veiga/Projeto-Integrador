import time
from machine import Pin, PWM
import uasyncio

pwm = PWM(Pin(25))
pwm.freq(50)
#x = 1/20 # Lowest value possible 5% Negative Duty


def Cpwm(dut):
    global pwm
    pwm.duty(dut)

def initEsc():
    time.sleep_ms(1500)
    print('Writing minimum output',end='\n')
    Cpwm(int(1/20 * 1023))
    time.sleep_ms(2000)
    print('Writing maximum output',end='\n')
    Cpwm(int(2/20 * 1023))
    print('Esc is Calibrated!\nNow you can enter any value between 0 and 1')
    time.sleep_ms(500)
    Cpwm(int(1/20 * 1023))


def loop():
    while True:
        try:
            y = float(input('Enter a number between 0 and 1: '))
            if y>=0 and y<=1:
                x = (y+1)/20
                duty = int(x*1023)
                Cpwm(duty)
            else:
                pass
        except KeyboardInterrupt:
            print("Program terminated")
            pwm.deinit()
            break

initEsc()

loop()
