import argparse
import requests
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup
from termcolor import colored
from os import path
from sys import exit
from datetime import datetime

def get_args():
    
    parser=argparse.ArgumentParser()
    
    
    parser.add_argument('-d','--domain',dest="target",
                        help="Domain to scan ",required=True)
    
    parser.add_argument('-t','-threads',dest="threads",
                        help="Specify the threads, (Default => 10)",type=int,default=10)
    
    parser.add_argument('-r', '--follow-redirect', dest="follow_redirect", action='store_true',
                        help="Follow redirects")
    
    parser.add_argument('-H', '--headers', dest="header", nargs='*',
                        help="Specify HTTP headers (e.g., -H 'Header1: val1' -H 'Header2: val2')")
    
    parser.add_argument('-a', '--useragent', metavar='string', dest="user_agent",default="SubBuster/1.0",
                        help="Set the User-Agent string (default 'SubBuster/1.0')")
    
    parser.add_argument('--ignore-code',dest='ignore_codes',
                        type=int,help="Codes to ignore",nargs='*')
    
    parser.add_argument('-ht', '--hide-title', dest="hide_title", action='store_true',
                        help="Hide response title in output")
    
    parser.add_argument('-mc', dest='match_codes', nargs='*',
                        help="Include status codes to match, separated by space (e.g., -mc 200 404)")
    
    parser.add_argument('-ms', dest='match_size', nargs='*',
                        help="Match response size, separated by space")
    
    parser.add_argument('-fc', dest="filter_codes", nargs='*',
                    help="Filter status codes, separated by space")
    
    parser.add_argument('-fs', nargs='*', dest='filter_size',
                    help="Filter response size, separated by space")
    
    parser.add_argument('-w','--wordlist',dest='wordlist',required=False,default='wordlist.txt',
                    help="Specify the wordlist to use !")

    try:
        return parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    
    arguments = get_args()
    
    target = arguments.target
    hide_title = arguments.hide_title or False
    redirection = arguments.follow_redirect or False
    user_agent = arguments.user_agent
    match_codes = arguments.match_codes
    match_size = arguments.match_size
    filter_codes = arguments.filter_codes
    filter_size = arguments.filter_size
    header = arguments.header
    wordlist = arguments.wordlist
    threads = arguments.threads

    if match_size and filter_size:
        print(colored(
            "[+] For now You can't use both match_size and filter_size", 'red'))
        exit()
    if match_codes and filter_codes:
        print(colored(
            "[+] For now You can't use both match_codes and filter_codes", 'red'))
        exit()
    if not path.exists(wordlist):
        print(colored("[-] Provide a valid wordlist file!", 'red'))
        exit()

    headers = {}
    if header:
        for h in header:
            key, value = h.split(':', 1)
            headers[key] = value.strip()
    headers['User-Agent'] = user_agent

    bruteforcer = SubdomainBruteforcer(target, wordlist, redirection, headers, match_codes, match_size, filter_codes, filter_size, hide_title, threads)
    bruteforcer.print_banner()
    bruteforcer.main()