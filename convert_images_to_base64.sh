for i in *.png; do echo "$(echo $i | cut -d'.' -f1) = b'$(base64 -w 0 $i)'" && echo ""; done >>data.py
