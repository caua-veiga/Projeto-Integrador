import time
from machine import Pin, PWM
import uasyncio

pwm = PWM(Pin(25))
pwm2 = PWM(Pin(15))
pwm2.freq(50)
pwm.freq(50)
#x = 1/20 # Lowest value possible 5% Negative Duty

def Cpwm1(dut):
    global pwm
    pwm.duty(dut)

def Cpwm2(dut):
    global pwm2
    pwm2.duty(dut)

def initEsc():
    time.sleep_ms(2000)
    print('Writing minimum output',end='\n')
    Cpwm1(int(1/20 * 1023))
    Cpwm2(int(1/20 * 1023))
    time.sleep_ms(2500)
    print('Writing maximum output',end='\n')
    Cpwm1(int(2/20 * 1023))
    Cpwm2(int(2/20 * 1023))
    print('Esc is Calibrated!\nNow you can enter any value between 0 and 1\n')
    time.sleep_ms(500)
    Cpwm1(int(1/20 * 1023))
    Cpwm2(int(1/20 * 1023))


def loop():
    while True:
        try:
            y = float(input('DIREITA Enter a number between 0 and 1: '))
            yy = float(input('ESQUERDA Enter a number between 0 and 1: '))
            print('')
            if y>=0 and y<=1:
                x = (y+1)/20
                xx = (yy+1)/20
                duty1 = int(x*1023)
                Cpwm1(duty1)
                duty2 = int(xx*1023)
                Cpwm2(duty2)
            else:
                pass
        except KeyboardInterrupt:
            print("Program terminated")
            pwm.deinit()
            pwm2.deinit()
            break

initEsc()

loop()
