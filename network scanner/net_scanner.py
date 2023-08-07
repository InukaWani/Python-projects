#!/usr/bin/env python

import scapy.all as scapy
import optparse

'''arp request'''

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="find mac address on target")
    options, arguments = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  # who has ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # set our mac address to broadcast address
    arp_request_broadcast = broadcast/arp_request  # append
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # response the arp/broadcast request

    client_list=[]
    for element in answered_list:
        client_dic = {"src ip":element[1].psrc,"client mac":element[1].hwsrc}
        client_list.append(client_dic) # append client dictionary in to the client list
        # print(element[1].psrc +"\t\t"+element[1].hwsrc) / psrc - src ip and hwsrc = client mac address -> this goes to pritn_result finction

    return client_list  #

def print_result(client_results):   # client_result == client_list
    print("IP\t\t\t MAC address")
    print("-----------------------------------------")
    for client in client_results:
        print(client["src ip"]+"\t\t"+client["client mac"])  # list of dictionary = keys


options = get_arguments()
client_list = scan(options.target)  # capture client list
print_result(client_list)  # print_result() -> scan



'''
    # arp_request.show()
    # broadcast.show()
    # arp_request_broadcast.show()
    # print(answered.summary()) - show what happening in print()
    # scapy.ls(scapy.ARP()) -> prints ARP fields
    # scapy.ls(scapy.Ether()) -> prints broadcast fields

'''

