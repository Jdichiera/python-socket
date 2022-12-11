# Import the libraries that we need to use sys and socket. Sys is used to parse
# command line arguments
import sys
from socket import *

# Declare the server address and port that my local server is listening on
serverName = '127.0.0.1'
serverPort = 12000

# Gather the arguments that were passed in when starting the client
host = sys.argv[1]
hostPort = int(sys.argv[2])
requestMethod = sys.argv[3]
requestPath = sys.argv[4]

# Create a client socket.
# AF_INET describes how the socket will be used SOCK_STREAM defines that a 
# connection based protocol will be used
clientSocket = socket(AF_INET, SOCK_STREAM)

# Attempt a connection to the servername and server port listed above
clientSocket.connect((serverName, serverPort))

# If the request is a GET then we want to send the appropriate message to the server
if requestMethod.upper() == 'GET':
    # Create the header to be sent
    header="GET /" + requestPath + " HTTP/1.0\r\n"

    # Encode the header and send it to the server
    clientSocket.send((header).encode())

    # Receive any response that is sent from the server
    # Ideally this would be done in an endless loop so we could make sure that
    # we have received everything, but after literally hours spent, I could not get it to work
    # Thus, we have the backup method - two receives :)
    serverResponse = clientSocket.recv(1024)
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
    
    # Open the file that we want to send and read the file into a variable that will be
    # used to send the data
    filetosend = open(requestPath, "rb")
    data = filetosend.read()
    clientSocket.sendall(data)

    # Close the file after we are done
    filetosend.close()

    # Print a message to the console and close the socket
    print("Done Sending.")
    clientSocket.close()