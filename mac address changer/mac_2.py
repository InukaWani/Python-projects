#!/usr/bin/env python

import subprocess  #subprocess module - we can execute shell commands by using this module
import optparse
import re    #regex
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")
    (options, arguments) = parser.parse_args()    # options store ex: eth0 and 00:11:22:33:44:55 | arguments store ex: --interface , --mac
    if not options.interface:  # user did not mention interface
        parser.error("[-] please specify a interface")   #error msg for interface
    elif not options.new_mac:
        parser.error("[-] please specify a mac address")   # error msg for mac-address
    return options

def change_mac(interface, new_mac):

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] changing mac address for " + interface + " to " + new_mac)
def get_current_mac(interface):

    ifconfig_result = subprocess.check_output(["ifconfig", interface]) #option. cant call within funnction
    ifconfig_output_str = ifconfig_result.decode("utf-8").strip()  # Decode and remove leading/trailing whitespace

    mac_addrs_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output_str))  # mac address regex search result

    if mac_addrs_search_result:
        return mac_addrs_search_result.group(0)  # print first match
    else:
        print("[-]could not read mac address")


options = get_arguments()  # capture options only beacuse not using arguments , change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface) #capture return value of get_current_mac function
print("current mac: " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface) #current mac

if current_mac == options.new_mac:
    print("mac address is changes successfully: " + current_mac)
else:
    print("mac address did not changed")


