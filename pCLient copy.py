# Import statements for system, JSON, requests, and socket
import sys
import json
import requests
from socket import *

# In this block I am reading in the arguments passed in the terminal
host = sys.argv[1]
hostPort = int(sys.argv[2])
requestMethod = sys.argv[3]
requestPath = sys.argv[4]

# When testing with the client only I used these commands
# if requestMethod.upper() == 'GET':
#     request = requests.get(host)
#     print(request.text)
    
# elif requestMethod.upper() == 'PUT':
#     headers = {'Content-type': 'text/plain'}
#     request = requests.put(host, data=open(requestPath, 'rb'), headers=headers)
# print(request.status_code)

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
# clientSocket.send(sentence.encode())
clientSocket.send(json.dumps({"host": host, "hostPort": hostPort, "requestMethod": requestMethod, "requestPath": requestPath}).encode())
modifiedSentence = clientSocket.recv(2048)
clientSocket.close()
print ('From Server:', modifiedSentence.decode())

