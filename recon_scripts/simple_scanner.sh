# source (inspired) -> bug bounty bootcamp book from Vickie Li -> chapter5/ Writing your own recon scrips 

#!/bin/bash
PATH_TO_DIRSEARCH="$HOME/tools/bugbounty/dirsearch"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
TODAY=${date}

echo "This scan was created on $TODAY"

echo "Creating directory $DIRECTORY"
mkdir $DIRECTORY

nmap $DOMAIN > $DIRECTORY/nmap.txt
echo "Results of nmap scanner saved in $DIRECTORY/nmap.txt"

# export PATH="PATH_TO_DIRSEARCH:$PATH"
touch $DOMAIN/dirsearch.txt
python3 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --format=simple -o $DOMAIN/dirsearch.txt
echo "Results of dirsearch saved in $DOMAIN/dirsearch.txt"