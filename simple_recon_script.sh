# source (inspired) -> bug bounty bootcamp book from Vickie Li -> chapter5/ Writing your own recon scrips 

#!/bin/bash
PATH_TO_DIRSEARCH="$HOME/tools/bugbounty/dirsearch"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
TODAY=${date}

echo "This scan was created on $TODAY"


if [ ! -d "$DIRECTORY" ]; then
 mkdir "$DIRECTORY"
 echo "Directory $DIRECTORY has been created."
fi

case $2 in
    nmap_only)
        nmap $DOMAIN > $DIRECTORY/nmap.txt
        echo "Results of nmap scanner saved in $DIRECTORY/nmap.txt."
        ;;
    dirsearch-only)
        # export PATH="PATH_TO_DIRSEARCH:$PATH"
        echo "\n" > $DOMAIN/dirsearch.txt
        python3 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --format=simple -o $DOMAIN/dirsearch.txt
        echo "Results of dirsearch saved in $DOMAIN/dirsearch.txt."
        ;;
    cert-only)
        curl "https://crt.sh/?q=%25.$DOMAIN&output=json" -o $DIRECTORY/cert.txt
        echo "Results of cert parsing is stored in $DIRECTORY/cert.txt."
        ;;
    *)
        nmap $DOMAIN > $DIRECTORY/nmap.txt
        echo "Results of nmap scanner saved in $DIRECTORY/nmap.txt."
        echo "\n" > $DOMAIN/dirsearch.txt
        python3 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --format=simple -o $DOMAIN/dirsearch.txt
        echo "Results of dirsearch saved in $DOMAIN/dirsearch.txt."
        curl "https://crt.sh/?q=%25.$DOMAIN&output=json" -o $DIRECTORY/cert.txt
        echo "Results of cert parsing is stored in $DIRECTORY/cert.txt."
        ;;
esac