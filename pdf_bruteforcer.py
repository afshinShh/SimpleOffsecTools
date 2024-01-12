from PyPDF2 import PdfFileReader, PdfFileWriter
from os import path
from sys import exit
from termcolor import colored

def bruteforcer(pdfFile, wordlistFile):
    passwords = []
    
    with open(wordlistFile,'r') as f:
        for password in f.readlines():
            passwords.append(password.strip())
    
    reader = PdfFileReader(pdfFile)
    for password in passwords:
        if str(reader.decrypt(password)) == 'PasswordType.OWNER_PASSWORD':
            print(colored(f"[+] Password Found: {password}", 'green', attrs=['bold']))
            return password

def decrypt_pdf(encrypted_file, decrypted_file_name, password):
    with open(encrypted_file, 'rb') as encryptedFile, open(decrypted_file_name, 'wb') as decryptedFile:
        reader = PdfFileReader(encryptedFile)
        if reader.is_encrypted:
            reader.decrypt(password)
            
        writer = PdfFileWriter()
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))
        writer.write(decryptedFile)
    print(colored(f"[+] File has been successfully Decrypted and Saved at: {decrypted_file_name}", 'cyan', attrs=['bold']))

if __name__ == "__main__":  
    pdfFile = input("Enter the location of the password protected pdf file: ") 
    if not path.exists(pdfFile):
        print(colored("[-] Please provide a valid pdf file location!",'red'))
        exit(1)

    wordlistFile = input("Enter the location of the wordlist file: ")
    if not path.exists(wordlistFile):
        print(colored("[-] Please provide a valid wordlist file location!",'red'))
        exit(1)
    
    password = bruteforcer(pdfFile, wordlistFile)
    if password:
        decrypt_pdf(pdfFile, f"decrypted-{path.basename(pdfFile)}", password)
    else:
        print(colored("[-] Password was not Found", 'red'))