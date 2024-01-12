from PyPDF2 import PdfFileReader, PdfFileWriter
from os import path
from termcolor import colored
from sys import exit

def load_passwords(wordlist_file):
    with open(wordlist_file, 'r') as f:
        return [password.strip() for password in f.readlines()]

def find_password(pdf_file, passwords):
    reader = PdfFileReader(pdf_file)
    for password in passwords:
        if str(reader.decrypt(password)) == 'PasswordType.OWNER_PASSWORD':
            return password
    return None

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

def main():
    pdf_file = input("Enter the location of the password-protected PDF file: ")
    wordlist_file = input("Enter the location of the wordlist file: ")

    if not path.exists(pdf_file):
        print(colored("[-] Please provide a valid PDF file location!", 'red'))
        exit(1)

    if not path.exists(wordlist_file):
        print(colored("[-] Please provide a valid wordlist file location!", 'red'))
        exit(1)

    passwords = load_passwords(wordlist_file)
    password = find_password(pdf_file, passwords)

    if password:
        decrypt_pdf(pdf_file, f"decrypted-{path.basename(pdf_file)}", password)
        print(colored(f"[+] Password Found: {password}", 'green', attrs=['bold']))
    else:
        print(colored("[-] Password was not Found", 'red'))

if __name__ == "__main__":
    main()
