import sys
import argparse
import time
from datetime import datetime
from termcolor import colored
from scapy.all import scapy
from multiprocessing import Process

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-vi', '--victimip', dest='victimip',
                        help="specify the ip address of the victim", required=True)
    parser.add_argument('-gi', '--gatewayip', dest='gatewayip',
                        help="specify the ip address of the gateway", required=True)
    parser.add_argument('-i', '--interface', dest='interface', default="eth0",
                        help="specify the interface to use (default=eth0)")
    parser.add_argument('-sniff',dest="sniff",
                        help="Specify if you want to only capture certain packets and get it in pcap file", required=False, action='store_true')
    parser.add_argument('-pc', metavar="packet count", dest='PacketCount', default=1000, type=int,
                        help="specify the packet count if you want to sniff! (sniff opetion required)", required=False)
    arguments = parser.parse_args()
    if arguments.sniff and arguments.packetCount <= 0:
        print(colored("[-] Packet count should be a positive integer when using the sniffing option!", 'red'))
        parser.print_help()
        sys.exit(1) 
    return arguments

def get_mac_addr(ip):
    pass

def poisening(victimIP, victimMac, gatewayIP, gatewayMac):
    pass

def sniffing(packetCount, interface):
    pass

if __name__ == "__main__":
    arguments = get_args()
    
    victimIP = arguments.victimip
    victimMac = get_mac_addr(victimIP)
    
    gatewayIP = arguments.gatewayip
    gatewayMac = get_mac_addr(gatewayIP)
    
    interface = arguments.interface
    packetCount = arguments.PacketCount
    
    print_banner(victimIP, victimMac, gatewayIP, gatewayMac, interface)
    
    poisening_process = Process(target=poisening, args=(victimIP, victimMac, gatewayIP, gatewayMac))
    poisening_process.start()
    
    if arguments.sniff:
        sniffing_process = Process(target=sniffing, args=(packetCount, interface))
        sniffing_process.start()