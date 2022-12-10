# Import sys, JSON (for sending values to the server), requests (for handling the get and put requests), and socket
# Note - requests was only used when testing the client alone
import sys
import json
# import requests
from socket import *

# Declare the server address and port that my server is listening on
serverName = '127.0.0.1'
serverPort = 12000

# Gather the arguments that were passed in when starting the client
host = sys.argv[1]
hostPort = int(sys.argv[2])
requestMethod = sys.argv[3]
requestPath = sys.argv[4]

# This block was used when testing the client alone
# if requestMethod.upper() == 'GET':
#     request = requests.get(host)
#     # print(request.text)
# elif requestMethod.upper() == 'PUT':
#     headers = {'Content-type': 'text/plain'}
#     request = requests.put(host, data=open(requestPath, 'rb'), headers=headers)

# Create a client socket.
# AF_INET describes how the socket will be used SOCK_STREAM defines that a 
# connection based protocol will be used
clientSocket = socket(AF_INET, SOCK_STREAM)

# Attempt a connection to the servername and server port listed above
clientSocket.connect((serverName, serverPort))

# If the request is a GET then we want to send the appropriate message to the server
if requestMethod.upper() == 'GET':
    # Send a message to the server. In this case I am encoding the outgoing message into JSON
    header="GET /" + requestPath + " HTTP/1.0\r\n"

    # Encode the header and send it to the server
    clientSocket.send((header).encode())

    # Receive any response that is sent from the server
    # Ideally this would be done in an endless loop so we could make sure that
    # we have received everything, but after literally hours spent, I could not get it to work
    # Thus, we have the backup method - two receives :)
    serverResponse = clientSocket.recv(1024)
    # print(serverResponse)
    response = serverResponse.decode()
    print(response)
    
    # This second response gets the content of the index page and prints it out
    serverResponse = clientSocket.recv(1024)
    response = serverResponse.decode()
    print(response)
    
    # Now that we have received the bits that we want to receive - close the socket
    clientSocket.close()

# If the request is a PUT then we want to send the a PUT message to the server
if requestMethod.upper() == 'PUT':
    # Create the PUT header and send it to the server
    header="PUT " + requestPath + "\r\n"
    clientSocket.send((header).encode())
    
    filetosend = open("test1.txt", "rb")
    data = filetosend.read()
    clientSocket.sendall(data)
    # while data:
    #     print("Sending...")
    #     clientSocket.send(data)
    #     data = filetosend.read(1024)
    #     print('data done')
    filetosend.close()
    # clientSocket.send(b"DONE")
    print("Done Sending.")
    # print(clientSocket.recv(1024).decode())
    clientSocket.close()




# If we have neither get nor put, just close the socket


# elif requestMethod.upper() == 'PUT':
#     filetosend = open("test1.txt", "rb")
#     data = filetosend.read(1024)
#     while data:
#         print("Sending...")
#         clientSocket.send(data)
#         data = filetosend.read(1024)
#     filetosend.close()
#     clientSocket.send(b"DONE")
#     print("Done Sending.")
#     print(clientSocket.recv(1024))
#     clientSocket.shutdown(1)
#     clientSocket.close()



