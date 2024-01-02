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

def print_banner(victimIp, victimMac, gatewayIp, gatewayMac):
    banner_line = "-" * 60
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    arp_start_message = f"Arp Poisoning starting at {timestamp}"

    print(banner_line)
    print(colored(arp_start_message, 'cyan', attrs=['bold']))
    print(banner_line)
    print(f"[*] Victim IP\t: {victimIp}")
    print(f"[*] Victim Mac\t: {victimMac}")
    print(f"[*] Gateway Ip\t: {gatewayIp}")
    print(f"[*] Gateway Mac\t: {gatewayMac}")
    print(banner_line)


def get_mac_addr(ip):
    
    '''
        an example:
    
    ARP Request Frame Details:
        ###[ ARP ]###
    hwtype    = 0x1
    ptype     = 0x800
    hwlen     = 6
    plen      = 4
    op        = who-has
    hwsrc     = 00:00:00:00:00:00
    psrc      = 0.0.0.0
    hwdst     = 00:00:00:00:00:00
    pdst      = 192.168.1.1

    Ethernet Frame Details:
    ###[ Ethernet ]###
    dst       = ff:ff:ff:ff:ff:ff
    src       = 00:00:00:00:00:00
    type      = 0x0

    Constructed ARP Ether Packet:
    ###[ Ethernet ]###
    dst       = ff:ff:ff:ff:ff:ff
    src       = 00:00:00:00:00:00
    type      = 0x806
    ###[ ARP ]###
        hwtype    = 0x1
        ptype     = 0x800
        hwlen     = 6
        plen      = 4
        op        = who-has
        hwsrc     = 00:00:00:00:00:00
        psrc      = 0.0.0.0
        hwdst     = 00:00:00:00:00:00
        pdst      = 192.168.1.1
        
    hwtype: Hardware type, indicating the type of hardware being used.
    ptype: Protocol type, specifying the type of protocol addresses used in the ARP message
    hwlen: Length of hardware addresses in bytes.
    plen: Length of protocol addresses in bytes. 
    op: Opcode, indicating the type of ARP message. (1=>Arp request / 2=>Arp Reply / 3=>Rarp request)
    hwsrc: Source hardware (MAC) address.
    psrc: Source protocol (IP) address.
    hwdst: Destination hardware (MAC) address.
    pdst: Destination protocol (IP) address.
    '''
    arp_request_frame = scapy.ARP(pdst=ip)
    ether_broadcast_frame = scap.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_ether_send_packet = ether_broadcast_frame / arp_request_frame
    response_packet = scapy.src(arp_ether_send_packet, timeout=1, retry=10, verbose=False)[0]
    return response_packet[0][1].hwsrc

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
        