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
    def __init__(self,target, wordlist, extensions, redirection, headers, match_codes, match_size, filter_codes, filter_size, outputfile, hide_title) -> None:
        self.target = target
        self.wordlist = wordlist
        self.extensions = extensions
        self.redirection = redirection
        self.headers = headers
        self.match_codes = match_codes
        self.match_size = match_size
        self.filter_codes = filter_codes
        self.filter_size = filter_size
        self.output = output
        self.hide_title = hide_title
        self.match_codes = match_codes
        self.match_size = match_size
        self.filter_codes = filter_codes
        self.filter_size = filter_size
        self.outputfile = outputfile
        self.hide_title = hide_title        
        
    def print_banner(self):
        from datetime import datetime
        print("-"*80)
        print(colored(
            f"Directory and file bruteforcer starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'cyan', attrs=['bold']))
        print("-"*80)
        print(colored("[*] Target Url".ljust(20, " "),
              'light_red'), ":", f"{self.target}")
        print(colored("[*] Wordlist".ljust(20, " "),
              'light_red'), ":", f"{self.wordlist}")
        if self.headers:
            print(colored("[*] Headers".ljust(20, " "),
                  'light_red'), ":", f"{headers}")
        if self.extensions:
            print(colored("[*] Extensions".ljust(20, " "),
                  'light_red'), ":", f"{self.extensions}")
        if self.outputfile:
            print(colored("[*] Output File".ljust(20, " "),
                  'light_red'), ":", f"{self.outputfile}")
        if self.match_size:
            print(colored("[*] Match Res size".ljust(20, " "), 'light_red'),
                  ":", f"{self.match_size}")
        if self.match_codes or self.filter_codes:
            if self.match_codes:
                print(colored("[*] Match Codes".ljust(20, " "),
                              'light_red'), ":", f"{self.match_codes}")
            if self.filter_codes:
                print(colored("[*] Filter Codes".ljust(20, " "), 'light_red'),
                      ":", f"{self.filter_codes}")
        else:
            print(colored("[*] Status Codes".ljust(20, " "),
                  'light_red'), ":", f"All Status Codes")

        if self.filter_size:
            print(colored("[*] Filter Response Size".ljust(20, " "), 'light_red'),
                  ":", f"{self.filter_size}")
        print("-"*80)
        print("-"*80)
            
    async def main(self):
        try:
            tasks = []
            dirs = []
            
            with open (self.wordlist, "r") as f:
                for word in f.readlines():
                    word = word.strip()
                    dirs.append(f'/{word}')
                    if self.extensions:
                        for ext in self.extensions:
                            dirs.append(f'/{word}.{ext}')
            
            async with aiohttp.ClientSession(headers=self.headers) as session:
                for dir in dirs:
                    tasks.append(asyncio.create_task(
                        self.brute_dir(word=dir, session=session)))
                    if len(tasks) >= 50:
                        await asyncio.gather(*tasks)
                        
        except aiohttp.ClientError as e:
            print(f"An error occurred during the HTTP request: {str(e)}")
        
        except KeyboardInterrupt:
            print("Process interrupted by keyboard")
            exit(0)
        
        except Exception as e:
            print(f"Unexpected Error: {e}")
            exit(1)          
        
    async def brute_dir(self, word, session):
        try:
            url = f"{self.target}{word}"
            async with session.get(url) as response:
                html = await response.text()

            response_length = str(len(html))
            status_code = str(response.status)
            url = url.split('://')[1]
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else []

            if await self.check_conditions(status_code, response_length):
                await self.print_and_save_output(status_code, response_length, url, title)

        except aiohttp.ClientError as err:
            print(f'An error occurred during the HTTP request: {str(err)}')
        
        except KeyboardInterrupt:
            print("Process interrupted by keyboard")
            exit(0)
        
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            exit(1)

    async def check_conditions(self, status_code, response_length):
        if self.match_codes:
            if status_code not in self.match_codes:
                return False
            if self.filter_size and response_length not in self.filter_size:
                return False
            if self.match_size and response_length not in self.match_size:
                return False
        elif self.filter_codes:
            if status_code in self.filter_codes:
                return False
            if self.filter_size and response_length not in self.filter_size:
                return False
            if self.match_size and response_length not in self.match_size:
                return False
        else:
            if self.filter_size and response_length not in self.filter_size:
                return False
            if self.match_size and response_length not in self.match_size:
                return False
        return True
    
    async def print_and_save_output(self, status_code, response_length, url, title):
        status_code = int(status_code)
        color = 'grey'
        if status_code >= 200 and status_code < 300:
            color = 'green'
        elif status_code >= 300 and status_code < 400:
            color = 'yellow'
        elif status_code >= 400 and status_code < 500:
            color = 'red'
        elif status_code > 500 and status_code < 600:
            color = 'magenta'

        status_code_str = str(status_code).ljust(9, " ")
        response_length_str = str(response_length).ljust(9)
        url_str = url.ljust(30)

        output = f"{colored(status_code_str, color)} {response_length_str} {url_str}"

        if not self.hide_title:
            output += f" [{title}]"

        print(output)

        if self.outputfile:
            with open(self.outputfile, 'a+') as f:
                f.write(
                    f"{status_code_str} {response_length_str} {url_str} [{title}]")

    
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
    