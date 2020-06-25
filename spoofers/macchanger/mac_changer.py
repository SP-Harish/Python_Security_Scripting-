#!usr/bin/env python

import subprocess

interface =input("interface> ")
newmac=input("enter the new macaddress> ")

print("[+]changing macaddress for "+interface+" to "+newmac)

# subprocess.call("ifconfig " + interface + " down",shell=True)             user will be able to execute his desired
# subprocess.call("ifconfig " +interface+ " hw ether "+ newmac,shell=True)  code along with the input.
# subprocess.call("ifconfig " +interface+ " up",shell=True)

subprocess.call(["ifconfig",interface,"down"])          #we treat it as a list. so any 
subprocess.call(["ifconfig",interface,"hw","ether",newmac])
subprocess.call(["ifconfig",interface,"up"])


