
#----- A simple TCP client program in Python using send() function -----

import socket
import time
import matplotlib.pyplot as plt

# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
clientSocket.connect(("172.20.10.5",80))

timestamp = [0.]
angles = [0.]

# fig = plt.figure()
# ax = fig.add_subplot()
# line, = ax.plot(timestamp, angles)
# fig.show()

while True:
    # Send data to server

    data = "Hello Server!"

    clientSocket.send(data.encode())

    # Receive data from server

    dataFromServer = clientSocket.recv(1024)


    # Print to the console

    # print(dataFromServer.decode("utf-8"))
    data = dataFromServer.decode("utf-8")
    print(data)
    # timestamp.append(timestamp[-1] + data["Time"])
    # angles.append(data["Angle"])
    # print(timestamp)
    # print(angles)
#    line.set_data(timestamp, angles)
 #   ax.draw()

    #clientSocket.detach()
    time.sleep(1)
