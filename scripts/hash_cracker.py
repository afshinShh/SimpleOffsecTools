import hashlib
from os import path
from termcolor import colored

class PasswordCracker:
    def __init__(self,hash_format):
        pass   

    def crack_password(self,common_passwords_file):
        pass
    
    
def main():
    hash_format = input("Enter the hash format (sha256, sha1, md5, etc): ")
    password = input("Enter the password to crack: ")
    common_paswords_file = input("Enter the location of the common passwords file: ")
    if not path.exists(common_paswords_file):
        print(colored("[-] Provide a valid wordlist file!",'red'))
        exit()
    
    hash_cracker = PasswordCracker(hash_format)
    cracked_password = hash_cracker.crack_password(common_paswords_file)
    if cracked_password:
        print("the password is: ", cracked_password)
    else:
        print("the password could not be cracked")
    
if __name__ == "__main__":
    main()