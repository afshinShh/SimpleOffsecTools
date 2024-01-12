import hashlib
from os import path
from termcolor import colored

class PasswordCracker:
   SUPPORTED_HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
   
   def __init__(self, hash_format):
       if hash_format not in self.SUPPORTED_HASHES:
           raise ValueError("Invalid hash format")
       self.hash_format = hash_format
       self.hashed_password = None 
       
   def hash_password(self, password):
       hasher = hashlib.new(self.hash_format)
       hasher.update(password.encode())
       self.hashed_password = hasher.hexdigest()
       
   def crack_password(self, common_passwords_file):
       try:
           with open(common_passwords_file) as f:
               common_passwords = [line.rstrip('\n') for line in f.readlines()]
       except FileNotFoundError:
           print(colored("[-] Provide a valid wordlist file!",'red'))
           return None

       for common_password in common_passwords:
           hasher = hashlib.new(self.hash_format)
           hasher.update(common_password.encode())
           hashed_common_password = hasher.hexdigest()
           if self.hashed_password == hashed_common_password:
               return common_password
       return None

def main():
   hash_format = input("Enter the hash format (md5, sha1, sha224, sha256, sha384, sha512): ")
   password = input("Enter the password to crack: ")
   common_passwords_file = input("Enter the location of the common passwords file: ")
   
   hash_cracker = PasswordCracker(hash_format)
   hash_cracker.hash_password(password)
   cracked_password = hash_cracker.crack_password(common_passwords_file)
   if cracked_password:
       print("The password is: ", cracked_password)
   else:
       print("The password could not be cracked")
   
if __name__ == "__main__":
   main()
