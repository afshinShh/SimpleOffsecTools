import socket, os, sys, argparse, subprocess
from termcolor import colored
from datetime import datetime

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port',dest='port', default=1337, required=False, type=int,
                        help="Port to listen on")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = get_args()
    pass