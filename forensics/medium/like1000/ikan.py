import tarfile
import os

START_TAR = "1000.tar"
OUTPUT_FILE = "all_filler.txt"

current_tar = START_TAR

with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
    while os.path.exists(current_tar):
        print(f"[+] Extracting {current_tar}")

        extract_dir = current_tar.replace(".tar", "")
        os.makedirs(extract_dir, exist_ok=True)

        with tarfile.open(current_tar) as tar:
            tar.extractall(path=extract_dir)

        filler_path = os.path.join(extract_dir, "filler.txt")
        if os.path.exists(filler_path):
            with open(filler_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                output.write(f"===== {current_tar} =====\n")
                output.write(content + "\n\n")

        # Cari file .tar berikutnya
        next_tar = None
        for file in os.listdir(extract_dir):
            if file.endswith(".tar"):
                next_tar = os.path.join(extract_dir, file)
                break

        if not next_tar:
            print("[!] Tidak ditemukan tar berikutnya, proses selesai.")
            break

        current_tar = next_tar

print("[✓] Semua filler.txt berhasil dikumpulkan ke all_filler.txt")
