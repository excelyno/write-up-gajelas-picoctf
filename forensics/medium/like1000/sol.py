import tarfile
import os

current_tar = "1000.tar"
step = 0

while True:
    step += 1
    print(f"[+] Step {step}: extracting {current_tar}")

    with tarfile.open(current_tar) as tar:
        tar.extractall(".")

    # hapus tar lama agar workspace bersih
    os.remove(current_tar)

    # cari tar berikutnya
    next_tar = None
    for f in os.listdir("."):
        if f.endswith(".tar"):
            next_tar = f
            break

    if next_tar:
        current_tar = next_tar
    else:
        print("[✓] Tidak ada tar lanjutan. Ini adalah layer terakhir.")
        break

print("\n[+] FILE TERSISA DI LAYER TERAKHIR:")
for f in os.listdir("."):
    print(" -", f)
