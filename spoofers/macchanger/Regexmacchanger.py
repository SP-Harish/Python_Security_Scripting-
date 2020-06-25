#!usr/bin/env python

import subprocess
import optparse
import re                       #library for using regex operations

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

def get_current_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", interface])  # check_out is used to capture the shell script
                                                                                # And is stored in ifconfig_results
    macaddress_search_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_results)  # from pythex.com got the regex
    # re.search searches for the regex given in the variable ifconfig_results
    if macaddress_search_results:  # if a value exists then
        return(macaddress_search_results.group(0))
    else:
        print("[+]please inter a valid interface")


options = parsearguments()
currentmac = get_current_mac(options.iface)
print("current mac address:"+str(currentmac))
if currentmac == options.nmac:
    print("current macaddress and the request macaddress appear to be same!")
else:
    change_mac(options.iface, options.nmac)
    currentmac= get_current_mac(options.iface)

    if currentmac == options.nmac:
        print("mac address successfully changed to:" + currentmac)
    else:
        print("[+]mac address was not changed")






