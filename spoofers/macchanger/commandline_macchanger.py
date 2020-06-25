#!usr/bin/env python

import subprocess
import optparse     #powerful library for parsing command-line options

parser= optparse.OptionParser()     #OptionParser is a class. and we create objectnamed parser.
parser.add_option("-i", "--interface", dest="iface", help="Interface to change the mac address")
parser.add_option("-m", "--mac", dest="nmac", help="new mac address to change")
#teaching the object what arguments to look for in the command line and storing that within function

(options,arguments)=parser.parse_args()     #to parse all the arguments/ this displays all the availble options.
                                            # (entered as arguments in the parser.add_options)

interface = options.iface   #assigning the command line arguments to the variables
newmac = options.nmac           #assigning the command line arguments to the variables

print("[+]changing macaddress for " +interface+ " to " +newmac)

subprocess.call(["ifconfig", interface, "down"])          #we treat it as a list.So, other command can be executed.
subprocess.call(["ifconfig", interface, "hw", "ether", newmac])
subprocess.call(["ifconfig", interface, "up"])


# Dest cannot be used directly because its a local variable within the functions. we need to assign it to interface and
#newmac.