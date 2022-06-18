# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
'''
import time
import network

ssid =  'Galaxy A32 5G1A70' #'iPhone Caua' #'UPTEC' #'Galaxy A32 5G1A70'
password = 'yfee4537' #'caualex12' #'UPTECNET'  #'yfee4537'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#print(wlan.scan())
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        time.sleep(0.1)
    print(' Connected!')
print('network config:', wlan.ifconfig())'''
