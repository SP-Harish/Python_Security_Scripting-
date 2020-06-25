#!/usr/bin/env python

import scapy.all as scapy

def scan(ip) :                                                      #used to get the targetip's mac address.
    arp_request = scapy.ARP(pdst=ip)                                 #crafting an arp packet.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")                #crafting broadcast packet to the router.
    arp_request_broadcast = broadcast / arp_request                 #appending broadcast packet and arp packet.
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]        #transmitting the packet using srp function. and storing the output in answered variable.
    return answered[0][1].hwsrc                                                      #extracting and returning the mac address part of the list element

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)   #sniff function is used to sniff all the packets in the given interface.

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:            #checking if the packet is a ARP packet and it is a ARP response(op=2)
        try:
            real_mac = scan(packet[scapy.ARP].psrc)                         #sending a broadcast request to the ip. and getting the original mac.
            response_mac = packet[scapy.ARP].hwsrc                          #mac present in the sniffed packet.

            if real_mac != response_mac:
                print("[+] your system is under attack!!!")
        except IndexError:
            pass

sniff("eth0")