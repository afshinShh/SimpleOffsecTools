# source -> bug bounty bootcamp book from Vickie Li -> chapter5/ Writing your own recon scrips 

#!/bin/bash
PATH_TO_DIRSEARCH="~/tools/bugbounty/dirsearch/"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon

echo "Creating directory $DIRECTORY"
mkdir $DIRECTORY

nmap $DOMAIN > $DIRECTORY/nmap.txt
echo "results of nmap scanner saved in $DIRECTORY/nmap.txt"

# export PATH="PATH_TO_DIRSEARCH:$PATH"
python3 $PATH_TO_DIRSEARCH/dirsearch.py -u $1 -e php  --simple-report $DOMAIN/dirsearch.txt
echo "results of dirsearch saved in $DOMAIN/dirsearch.txt"