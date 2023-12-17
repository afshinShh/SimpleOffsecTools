import argparse 
from termcolor import colored,cprint 


def get_args():
    """Function to get command-line arguments""" 
    parser = argparse.ArgumentParser()

    parser.add_argument("-n","--name", type=str)
    parser.add_argument("-p","--port", type=int,default=22)
    parser.add_argument("target",
                        help="Host to attack on e.g. 192.168.1.1")
    parser.add_argument("-u","--user", dest='username',required=True
                        ,help="Username which we want to bruteforce to ")
    
    argument= parser.parse_args()
    
    return argument

