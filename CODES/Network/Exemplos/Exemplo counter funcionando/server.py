import machine
#import datetime
import json

def do_connect():
    '''
    Input must be a tuple: (essid, password)
    '''
    import network

    essid =  'iPhone Caua' #'UPTEC' #'Galaxy A32 5G1A70'
    password =  'caualex12' #'UPTECNET'  #'yfee4537'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


count = 0
def requested():
    global count
    count += 1
    #'Time Requested': datetime.datetime.now(),
    data = {'Request number': count}

    return json.dumps(data)


def main():
    do_connect()

    import socket
    # Create a stream based socket(i.e, a TCP socket)

    # operating on IPv4 addressing scheme

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);



    # Bind and listen

    serverSocket.bind(("172.20.10.5",80));

    serverSocket.listen();

    # Accept connections

    while(True):


        (clientConnected, clientAddress) = serverSocket.accept();
        print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));



        dataFromClient = clientConnected.recv(1024)

        print(dataFromClient.decode());



        # Send some data back to the client

        data = requested()

        clientConnected.send(data.encode("utf-8"));
        #clientConnected.sendall(bytes(data,encoding="utf-8"))


if __name__=='__main__':
    main()
