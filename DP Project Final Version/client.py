#DEFENSIVE PROGRAMMING PROJECT FINAL VERSION
#Justin Sanner, Kayla Fortune, Michael Hopkins
#CLIENT
#VERSION DATE: 11/08/2020


#Initialization
import socket

#Connect to server
s = socket.socket()
s.connect(('127.0.0.1',12345))

#Loop that checks for server statements
while True:
    statement = (s.recv(2048).decode())
    print(statement)

    #Checks if last charicter is a space or if statement is "Good bye!"
    try:
        lastChar = statement[-1]
        if lastChar == " ":      #If last character is a space, get input from client and send it to server
            str = input("")
            s.send(str.encode());
        if statement == "Good bye!": #If statement is "Good bye!", close the client.
            s.close()
            exit(0)
    except IndexError:  #If neither are true or if statement returns index error, passes the check.
        pass
