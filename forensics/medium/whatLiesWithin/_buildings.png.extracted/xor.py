for k in {1,255}: do
  python3 - << EOF
data=open("out.bin","rb").read()
out=bytes(b^$k for b in data)
if b"picoCTF" in out:
    print("KEY =", $k)
    print(out.decode(errors="ignore"))
    exit()
EOF
done
