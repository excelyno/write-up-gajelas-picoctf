wget https://artifacts.picoctf.net/c/537/disko-1.dd.gz
gzip -d disko-1.dd.gz 
strings disko-1.dd | grep  "picoCTF"
