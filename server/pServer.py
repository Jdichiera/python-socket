# Import the libraries that I need. Sockets will allow me to make sockets and 
# exists allows me to check to see if the file that is being requested
# is on the server
from socket import *
from os.path import exists

# This is the port where the server will listen on
serverPort = 12000

# Select the socket that will be used
# AF_INET describes how the socket will be used SOCK_STREAM defines that a 
# connection based protocol will be used
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the address that I use to communicate with this server application
serverSocket.bind(("127.0.0.1", serverPort))

# Listen for a single connection
serverSocket.listen(1)

# Print some output so we know that the server is ready
print("The server is ready to receive")

# Waits for a connection
while True:
    # Accept an incoming request when it is detected
    connectionSocket, addr = serverSocket.accept()

    # Decode the message that is received from the client
    requestObject = connectionSocket.recv(1024).decode('utf8')

    # Split up the received object into a collection
    string_list = requestObject.split(' ')

    # Store the request type and file name in variables
    requestType = string_list[0]

    # If we are performing a GET we want to have the filepath formatted correctly so we check
    # for formatting and then prepend './' if we need to
    # We also extract the filename into a variable for use later
    if (string_list[1][0] == '/'):
        fileName = string_list[1].replace('/','')
        filePath = '.' + string_list[1]
    else:
        fileName = string_list[1]
        filePath = './' + string_list[1]
    
    # create a few variables which can be used to make our code more readable
    header = ''
    header1 = ''
    header2 = ''
    fileLength = 0
    outgoingHeader = ''
    outgoingContent = ''

    # If our request is a GET
    if (requestType.upper() == 'GET'):
        print('GET command for ' + fileName)

        # Check to make sure the file is on the server
        if (exists(filePath)):
            print(fileName + ' exists on server ... sending to client');

            # If the file is there, then we want to open it and read the contents
            buffer = open(filePath, 'rb')
            file = buffer.read()
            fileLength = len(file)
            buffer.close()

            # Form the correct header to transfer the file
            header="HTTP/1.1 200 OK\r\n" 
            header1="Content-Type: text/html\r\n" 
            header2="Content-Length: {}\r\n\r\n".format(fileLength)

            # set the contents of the file into the outgoing message
            outgoingContent = file;
        
        # If the file does not exist on the server then we want to send a different header
        # And set an appropriate outgoing message to notify the client
        else:
            print(fileName + ' does not exist on server ... notifying client');
            header="HTTP/1.1 404 Not Found\r\n" 
            header1="Content-Type: text/html\r\n" 
            header2="Content-Length: {}\r\n".format(fileLength) 
            outgoingContent = 'File Not Found on Server'
            
        # Concatenate the header that was formed above, and send it to the client
        outgoingHeader = header+header1+header2
        connectionSocket.send(outgoingHeader.encode())
 
 
    # If our request is a PUT request
    if (requestType.upper() == "PUT"):
        print('PUT command for ' + fileName)

        # Receive the data that we want to write to the file
        dataToWrite = connectionSocket.recv(2056)

        # I spent many hours rewriting this section because every
        # file that was written would have two question marks appended to the
        # end of the file name. ex: 'test.txt??'. This is a hacky way to 
        # have a usable file extension
        with open(fileName.split('.')[0] + '.txt','w') as f:
            f.write(dataToWrite.decode())

        # Close the file when we are done
        f.close()

        # Send a nice message to the client
        outgoingContent = 'Received file'
        
    # try to encode and send. If this throws an exception the outgoing message is already encoded
    # and we can just send it without encoding
    try:
        connectionSocket.sendall(outgoingContent.encode())
    except (UnicodeDecodeError, AttributeError):
        connectionSocket.sendall(outgoingContent)
    
    # Close up the shop and shut down the server
    print('closing socket')
    connectionSocket.close()
    print('ending program')
    exit()