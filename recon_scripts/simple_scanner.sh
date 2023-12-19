# source -> bug bounty bootcamp book from Vickie Li -> chapter5/ Writing your own recon scrips 

#!/bin/bash
echo "Creating directory $1_recon"
mkdir $1_recon

nmap $1 > $1_recon/nmap.txt
echo "results of nmap scanner saved in $1_recon/nmap.txt"

# export PATH="PATH_TO_DIRSEARCH:$PATH"
python3 ~/tools/bugbounty/dirsearch.py -u $1 -e php  --simple-report $1_recon/dirsearch.txt
echo "results of dirsearch saved in $1_recon/dirsearch.txt"