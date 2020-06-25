#!usr/bin/env python

import subprocess
import optparse


def parsearguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="iface", help="Interface to change the mac address")
    parser.add_option("-m", "--mac", dest="nmac", help="new mac address to change")
    (options,arguments)= parser.parse_args()
    if not options.iface:
        parser.error("please specify interface")
    if not options.nmac:
        parser.error("please specify macaddress")
    return options


def change_mac(interface, newmac):
    print("[+]changing macaddress for " + interface + " to " + newmac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newmac])
    subprocess.call(["ifconfig", interface, "up"])




(options)=parsearguments()
change_mac(options.iface, options.nmac)