from datetime import datetime
import argparse
import socket
import re
import concurrent.futures
from queue import Queue
import scapy.all as scapy
from termcolor import colored

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target URL or IP address")
    parser.add_argument(
        "-arp",
        dest="arp",
        help="Use this for ARP ping!",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-pT",
        dest="tcpPortScan",
        help="TCP Port Scan",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-pU",
        dest="udpPortScan",
        help="UDP Port Scan",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--ports",
        dest="ports",
        help="Port range to scan, default is 1-65535 (all ports)",
        required=False,
        action="store",
        default="1-65535",
    )
    parser.add_argument(
        "-t",
        "--threads",
        dest="threads",
        help="Threads for speed, default is 100",
        required=False,
        action="store",
        default=100,
        type=int,
    )
    return parser.parse_args()




def main():
    args = get_args()
    host = args.target
    start_port, end_port = map(int, args.ports.split("-"))
    scan_type = ""
    port_queue = Queue()
    print(colored("-"*65, 'cyan', attrs=['dark']))
    print(colored(
            f"\tNetwork scanner starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'cyan', attrs=['dark']))
    print(colored("-"*65, 'cyan', attrs=['dark']))

    if args.arp:
        print(colored("-"*50,'light_red'))
        print(colored("\tARP Ping Scan Results",'light_red'))
        print(colored("-"*50,'light_red'))
        print(colored("="*30,'black'))
        print(colored("\tPort\tState",'black',attrs=['bold']))
        print(colored("="*30,'black'))
        arp_ping(host)
        
    if ((args.tcpPortScan)or(args.udpPortScan)):
        print(colored("-"*50,'light_red'))
        if args.tcpPortScan:
            print(colored("\tTCP Port Scan Results",'light_red'))
            scan_type="T"
        elif (args.udpPortScan):
            print(colored("\tUDP Port Scan Results",'light_red'))
            scan_type="U"
        print(colored("-"*50,'light_red'))
        print()
        print(colored("="*30,'dark_grey'))
        print(colored("\tPort\tState",'dark_grey',attrs=['bold']))
        print(colored("="*30,'dark_grey'))
        
        
        for port in range(start_port, end_port + 1):
            port_queue.put(port)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.threads
        ) as executor:
            for _ in range(args.threads):
                executor.submit(scan_thread, host, scan_type, port_queue)
        port_queue.join()

if __name__ == "__main__":
    main()