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

nmap_scan()
{
    nmap $DOMAIN > $DIRECTORY/nmap.txt
    echo "Results of nmap scanner saved in $DIRECTORY/nmap.txt."
}

dirsearch_scan()
{
    # export PATH="PATH_TO_DIRSEARCH:$PATH"
    echo "\n" > $DOMAIN/dirsearch.txt
    python3 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --format=simple -o $DOMAIN/dirsearch.txt
    echo "Results of dirsearch saved in $DOMAIN/dirsearch.txt."
}
certscan()
{
    curl "https://crt.sh/?q=%25.$DOMAIN&output=json" -o $DIRECTORY/cert.txt
    echo "Results of cert parsing is stored in $DIRECTORY/cert.txt."
}
case $2 in
    nmap_only)
        nmap_scan
        ;;
    dirsearch-only)
        dirsearch_scan
        ;;
    cert-only)
        cert_scan
        ;;
    *)
        nmap_scan   
        dirsearch_scan
        cert_scan
        ;;
esac