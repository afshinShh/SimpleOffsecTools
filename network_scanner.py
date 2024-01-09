from datetime import datetime
import argparse
import queue
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
    def print_network_scanner_start():
        print(colored("-" * 65, 'cyan', attrs=['dark']))
        print(colored(f"\tNetwork scanner starting at {get_current_time()}", 'cyan', attrs=['dark']))
        print(colored("-" * 65, 'cyan', attrs=['dark']))

    def get_current_time():
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def print_arp_ping_scan_results():
        print(colored("-" * 50, 'light_red'))
        print(colored("\tARP Ping Scan Results", 'light_red'))
        print(colored("-" * 50, 'light_red'))
        print(colored("=" * 30, 'black'))
        print(colored("\tPort\tState", 'black', attrs=['bold']))
        print(colored("=" * 30, 'black'))

    def determine_scan_type(args):
        if args.tcpPortScan:
            return "T"
        elif args.udpPortScan:
            return "U"

    def print_port_scan_results_header(scan_type):
        print(colored("-" * 50, 'light_red'))
        print(colored(f"\t{scan_type} Port Scan Results", 'light_red'))
        print(colored("-" * 50, 'light_red'))
        print()
        print(colored("=" * 30, 'dark_grey'))
        print(colored("\tPort\tState", 'dark_grey', attrs=['bold']))
        print(colored("=" * 30, 'dark_grey'))

    def execute_port_scan_threads(args, host, scan_type, start_port, end_port):
        port_queue = prepare_port_queue(start_port, end_port)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            for _ in range(args.threads):
                executor.submit(scan_thread, host, scan_type, port_queue)
        port_queue.join()

    def prepare_port_queue(start_port, end_port):
        port_queue = Queue()
        for port in range(start_port, end_port + 1):
            port_queue.put(port)
        return port_queue
    
    def scan_thread(host, scan_type, port_queue):
        while True:
            try:
                port = port_queue.get_nowait()
                port_scan(port, host, scan_type)
                port_queue.task_done()
            except queue.Empty:
                break
    
    def port_scan(port, host, scan_type):
        socket_type = socket.SOCK_STREAM if scan_type == "T" else socket.SOCK_DGRAM    
        try:
            client = socket.socket(socket.AF_INET, socket_type)
            client.settimeout(0.5)
            client.connect((host, port))
            print(f"[*]\t{port}\tis Open")
            client.close()
        except KeyboardInterrupt:
            print(colored("[-] Keyboard interrupt detected, exiting!",'red', attrs=['bold']))
            exit(1)
        except:
            pass
    
    def arp_ping(ip):
        # only Valid IPv4 Addresses
        if not re.match(r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", ip):
            print(colored("[-] Please provide a valid IP address range for ARP ping!",'red',attrs=['bold']))
            exit(1)
        try:
            arp_request_frame = scapy.ARP(pdst=ip)
            broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            broadcast_frame_arp = broadcast_frame / arp_request_frame
            active_clients = scapy.srp(broadcast_frame_arp, timeout=2, verbose=False)[0]
            
            for _, reply in active_clients:
                print(f"[+]\t{reply.psrc}\t{reply.hwsrc}")
        except Exception as e:
            print(colored(f"[-] {e}",'red', attrs=['bold']))
            exit(1)
        
    ###################################################################################
    args = get_args()
    host = args.target
    start_port, end_port = map(int, args.ports.split("-"))
    print_network_scanner_start()

    if args.arp:
        print_arp_ping_scan_results()
        arp_ping(host)

    if args.tcpPortScan or args.udpPortScan:
        scan_type = determine_scan_type(args)
        print_port_scan_results_header(scan_type)
        execute_port_scan_threads(args, host, scan_type, start_port, end_port)
    ###################################################################################           
if __name__ == "__main__":
    main()