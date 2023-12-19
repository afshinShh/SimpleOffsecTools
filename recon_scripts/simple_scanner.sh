# source -> bug bounty bootcamp book from Vickie Li -> chapter5/ Writing your own recon scrips 

#!/bin/bash

nmap $1

# export PATH="PATH_TO_DIRSEARCH:$PATH"
python3 ~/tools/bugbounty/dirsearch.py -u $1 -e php
