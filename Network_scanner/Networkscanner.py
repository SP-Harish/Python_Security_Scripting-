#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    arp_request= scapy.ARP(pdst=ip)                     #crafting an arp packet.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")    #crafting broadcast packet to the router.
    arp_request_broadcast = broadcast / arp_request     #appending broadcast packet and arp packet.
    answered = scapy.srp(arp_request_broadcast, timeout=1 ,verbose=False)[0]            #transmitting the packet using srp function. and storing the output in answered variable.


    client_list = []                                # creating a list named client_list
    for element in answered:
        client_dic = {"IP": element[1].psrc
                      ,"mac": element[1].hwsrc}     # adding each element in the ansered(list) in the form of dict.
        client_list.append(client_dic)              # appending each dict element to the client_list
    return(client_list)

def print_result(results_list):
    print("IP adresss\t\tMac_Address\n==========================================")
    for client in results_list:
        print(client["IP" ]+ "\t\t" + client["mac"])    # printing using the key index


# target_iprange = get_argumets()
result_list =scan("10.1.1.1/24")                         #input your ip address range/ target ip.
print_result(result_list)
