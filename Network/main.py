def do_connect():
    '''
    Input must be a tuple: (essid, password)
    '''
    import network

    essid = 'Galaxy A32 5G1A70'
    password = 'yfee4537'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


if __name__=='__main__':
    do_connect()
