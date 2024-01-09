import requests
import argparse
from termcolor import colored
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',
                        help="Target URL or IP address, provide it along http/https",required=True)
    parser.add_argument('-d','--depth',dest='depth',type=int, default=1,
                        help="Depth of crawling, default is 1")
    return parser.parse_args()

class WebCrawler:
    def __init__(self, url, max_depth):
        self.url = url
        self.max_depth = max_depth
        self.subdomains = set()
        self.links = set()
        self.jsfiles = set()
        
    def print_banner(self):
        print("-" * 80)
        print(colored(f"Recursive Web Crawler starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'cyan', attrs=['bold']))
        print("-" * 80)
        print(f"[*] URL".ljust(20, " "), ":", self.url)
        print(f"[*] Max Depth".ljust(20, " "), ":", self.max_depth)
        print("-" * 80)
        
    def print_results(self):
        if self.subdomains:
            for subdomain in self.subdomains:
                print(f"[+] Discovered subdomain: {subdomain}")
        print()
        if self.links:
            for link in self.links:
                print(f"[+] Discovered link: {link}")
        print()
        if self.jsfiles:
            for jsfile in self.jsfiles:
                print(f"[+] Discovered JavaScript file: {jsfile}")
            
    def start_crawling(self):
        pass


if __name__ == '__main__':
    args = get_args()
    web_crawler = WebCrawler(args.url, args.depth)
    web_crawler.print_banner()
    web_crawler.start_crawling()
    web_crawler.print_results()