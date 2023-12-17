import argparse 
from termcolor import colored,cprint 
import asyncio 
import os

def get_args():
    """Function to get command-line arguments""" 
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


if __name__ == "__main__":
    print(colored("Afshin Here!!!","green"))
    cprint("Welcome to my SSH Bruteforcer","blue")
    
    arguments = get_args()
    
    if not os.path.exists(arguments.wordlist):
        print(colored(
            "[-] Wordlist location is not right","red"))
        exit(1)
        
    print("\n--------------------------------------------------------\n--------------------------------------------------------")
    print(colored(f"[*] Target\t: ", "magenta"), arguments.target)
    print(colored(f"[*] Username\t: ", "magenta"), arguments.username)
    print(colored(
        f"[*] Port\t: ", "magenta"), end="")
    print('22' if not arguments.port else arguments.port)
    print(
        colored(f"[*] Wordlist\t: ", "magenta"), end="")
    print(arguments.wordlist)
    print(colored(f"[*] Protocol\t: ", "magenta"), end="")
    print("SSH")
    print("--------------------------------------------------------\n--------------------------------------------------------")
    
    print(colored(
        f"SSH-Bruteforce starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'yellow'))
    print("\n--------------------------------------------------------\n--------------------------------------------------------")
    #asyncio.run(main(arguments.target, arguments.port,
    #            arguments.username, arguments.wordlist))
    
    