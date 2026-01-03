#!/usr/bin/env python3
import re
import base64
import subprocess
import zipfile

PCAP_FILE = "dump.pcap"
ZIP_FILE = "flag.zip"

def get_candidate_strings():
    # ambil semua printable strings dari pcap
    result = subprocess.check_output(["strings", PCAP_FILE], text=True)
    
    # cari pola yang “mirip” base64 (panjang > 20)
    candidates = re.findall(r"[A-Za-z0-9+/=]{20,}", result)
    return candidates

def clean_base64(s):
    # buang karakter yang tidak valid base64
    return re.sub(r"[^A-Za-z0-9+/=]", "", s)

def try_decode(s):
    try:
        return base64.b64decode(s).decode("utf-8", errors="ignore")
    except Exception:
        return None

def try_zip_password(password):
    try:
        with zipfile.ZipFile(ZIP_FILE) as z:
            z.extractall(pwd=password.encode())
        print(f"[OK] Password ditemukan: {password}")
        return True
    except Exception:
        return False

def main():
    print("[*] Men-scan pcap untuk kandidat base64...")
    candidates = get_candidate_strings()

    tested = set()

    for c in candidates:
        c = clean_base64(c)

        if c in tested:
            continue
        tested.add(c)

        decoded = try_decode(c)
        if not decoded:
            continue

        print(f"[>] Kandidat decode: {decoded}")

        # coba langsung sebagai password
        if try_zip_password(decoded.strip()):
            print("[+] Flag berhasil diekstrak!")
            return

    print("[-] Tidak ada password yang cocok. Cek ulang file pcap / zip.")

if __name__ == "__main__":
    main()
