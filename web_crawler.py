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
        def print_discovered(name, items):
            if items:
                print()
                for item in items:
                    print(f"[+] Discovered {name.capitalize()}: {item}")
        
        print_discovered("subdomain", self.subdomains)
        print_discovered("link", self.links)
        print_discovered("JavaScript file", self.jsfiles)
            
    def start_crawling(self):
        self._crawl(self.url, depth=1)
        
    def _crawl(self, url, depth):
        if depth > self.max_depth:
            return
        try:
            response = requests.get(url, timeout=3, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as err:
            print(f"[-] An error occurred: {err}")
            return

        subdomain_query = r"https?://([a-zA-Z0-9.-]+)"
        for link in soup.find_all('a', href=True):
            link_text = link.get('href')
            if link_text:
                if re.match(subdomain_query, link_text) and link_text not in self.subdomains:
                    self.subdomains.add(link_text)
                else:
                    full_link = urljoin(url, link_text)
                    if full_link != url and full_link not in self.links:
                        self.links.add(full_link)
                        self._crawl(full_link, depth + 1)

        for file in soup.find_all('script', src=True):
            script_src = file.get('src')
            if script_src:
                self.jsfiles.add(script_src)


if __name__ == '__main__':
    args = get_args()
    web_crawler = WebCrawler(args.url, args.depth)
    web_crawler.print_banner()
    web_crawler.start_crawling()
    web_crawler.print_results()