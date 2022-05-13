
import time
from machine import Pin, ADC, PWM


pwm = PWM(Pin(5))
pwm.freq(700)

dt1 = int(0.07*1024)
print(dt1)
pwm.duty(512)

while True:
    pass

pwm.deinit()
