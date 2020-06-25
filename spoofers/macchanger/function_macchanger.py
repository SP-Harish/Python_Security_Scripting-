#!usr/bin/env python

import subprocess
import optparse


def parsearguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="iface", help="Interface to change the mac address")
    parser.add_option("-m", "--mac", dest="nmac", help="new mac address to change")
    return parser.parse_args()

def change_mac(interface, newmac):
    print("[+]changing macaddress for " + options.iface + " to " + options.nmac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newmac])
    subprocess.call(["ifconfig", interface, "up"])




(options,arguments)=parsearguments()
change_mac(options.iface, options.nmac)