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