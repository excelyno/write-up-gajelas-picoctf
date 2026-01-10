import zlib

data = open("29.zlib", "rb").read()

found = False

for i in range(0, 200):
    try:
        out = zlib.decompress(data[i:])
        open("out.bin", "wb").write(out)
        print(f"[OK] zlib normal berhasil di offset {i}")
        found = True
        break
    except:
        try:
            out = zlib.decompress(data[i:], -zlib.MAX_WBITS)
            open("out.bin", "wb").write(out)
            print(f"[OK] raw deflate berhasil di offset {i}")
            found = True
            break
        except:
            pass

if not found:
    print("[-] Tidak ditemukan stream zlib sampai offset 200")
