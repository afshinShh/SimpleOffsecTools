import argparse
from bs4 import BeautifulSoup
from sys import exit 
from termcolor import colored
from os import path
import asyncio
import aiohttp


def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-u', '--url', dest='target',
                        help='Target URL (provide it with http/https)', required=True)
    
    parser.add_argument('-x', dest='extensions', nargs='*',
                        help='Extensions to search for (e.g., php asp)')
    
    parser.add_argument('-r', '--follow-redirection',dest='follow-redirect', action='store_true',
                        help='follow redirects')
    
    parser.add_argument('-H', '--headers', dest='header', nargs='*',
                        help='Headers to send with the request (e.g., -H "Header1: val1" -H "Header2: val2")')
    
    parser.add_argument('-a', '--useragent', metavar='string', dest='user_agent', default='directory_buster/1.0',
                        help='Set the User-Agent string (default "directory_buster/1.0")')
    
    parser.add_argument('-ht', '--hide-title', dest='hide_title', action='store_true',
                        help='Hide the response title in the output')
    
    parser.add_argument('-mc', '--match-codes', nargs='*',
                        help='Match response codes separated by space(e.g., -mc 200 301)')
    
    parser.add_argument('-ms', '--match-size', nargs='*',
                        help='Match response size separated by space (e.g., -ms 100 200)')
    
    parser.add_argument('-fc', dest="filter_codes", nargs='*', default=["404"],
                        help="Filter status codes, separated by space")
    
    parser.add_argument('-fs', nargs='*', dest='filter_size',
                        help="Filter response size, separated by space")
    
    parser.add_argument('-w', '--wordlist', dest='wordlist',
                        help='Path to the wordlist file to use for fuzzing', required=True)
    
    parser.add_argument('-o', '--output', dest='output',
                        help='Path to the output file to save the results')
    
    try:
        return parser.parse_args()
    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)
        
        
class DirBruteforcer():
    def __init__(self,target, wordlist, extensions, redirection, headers,
                            match_codes, match_size, filter_codes, filter_size, output, hide_title) -> None:
            pass
    
    def print_banner(self):
        pass
    
    async def main(self):
        pass
        
if __name__ == "__main__":
    
    arguments = get_args()
    
    target = arguments.target
    extensions = arguments.extensions 
    hide_title = arguments.hide_title or False
    redirection = arguments.follow_redirect or False
    useragent = arguments.user_agent 
    match_codes = arguments.match_codes  
    match_size = arguments.match_size
    filter_codes = arguments.filter_codes
    filter_size = arguments.filter_psize
    output = arguments.output
    header = arguments.header
    wordlist = arguments.wordlist
    
    if match_size and filter_size:
        print(colored("[+] For now You can't use both match_size and filter_size", "red"))
        exit(1)
    
    if match_codes and filter_codes:
        print(colored("[+] For now You can't use both match_codes and filter_codes", "red"))
        exit(1)
    
    if not path.exists(wordlist):
        print(colored("[-] Provide a valid wordlist file!", 'red'))   
        exit(1)
        
    headers = {}
    if header:
        for h in header:
            key, value = h.split(":", 1)
            headers[key] = value.strip()
    headers['User-Agent'] = useragent
    
    bruteforcer = DirBruteforcer (target, wordlist, extensions, redirection, headers,
                                match_codes, match_size, filter_codes, filter_size, output, hide_title)
    bruteforcer.print_banner()
    asyncio.run(bruteforcer.main())
    