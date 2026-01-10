🛡️ The Ultimate Digital Forensics & CTF Field ManualVersion: 2.0 (Deep Technical)Target: CTF Players, Incident Responders, Forensic AnalystsObjective: Panduan end-to-end dari triase hingga deep-dive analysis.🧠 I. Filosofi & Mental Model (Deep Dive)1. The Data Structure TheoryDalam dunia digital, tidak ada "magic". Semua file hanyalah sekumpulan bytes (00-FF).Structured Data: Mengikuti spesifikasi format (Header, Body, Footer).Unstructured/Hidden Data: Data yang disisipkan di slack space, komentar metadata, atau diobfuskasi.Entropy: Ukuran keacakan data.Entropy Rendah: Teks, HTML, Source Code (banyak pola berulang).Entropy Tinggi: File terkompresi, Terenkripsi, atau random bytes.Analisis: Gunakan binwalk -E untuk melihat grafik entropy. Jika ada blok entropy tinggi di tengah file gambar, kemungkinan ada data terenkripsi di dalamnya.2. The Chain of ValidationSetiap temuan harus divalidasi dengan metode berbeda.Jika file command mengatakan JPEG, validasi dengan xxd (Hex) untuk melihat FF D8 FF.Jika gambar terlihat biasa, cek integritas CRC checksum-nya (pngcheck).3. Workflow Investigasi (OODA Loop)Observe: Kumpulkan file, hash, dan metadata dasar.Orient: Tentukan jenis file sebenarnya dan potensi vektor (Stego? Malware? Log?).Decide: Pilih tools yang tepat (Static Analysis vs Dynamic Analysis).Act: Eksekusi tool, ekstrak data, dan catat hasil.🔍 II. Fase 0: Initial Triage & FingerprintingTujuan: Mengidentifikasi "apa" sebenarnya file ini tanpa mengeksekusinya (Static Analysis).2.1 File Signature Analysis (Magic Bytes)Jangan percaya ekstensi. Ekstensi hanyalah petunjuk bagi OS untuk memilih aplikasi pembuka. Identitas asli ada di header.Database Magic Bytes Umum:| Format | Signature (Hex) | ASCII | Trailer/Footer (Hex) || :--- | :--- | :--- | :--- || JPEG | FF D8 FF E0 | ... | FF D9 || PNG | 89 50 4E 47 0D 0A 1A 0A | .PNG.... | 49 45 4E 44 AE 42 60 82 (IEND) || GIF | 47 49 46 38 39 61 | GIF89a | 00 3B || ZIP | 50 4B 03 04 | PK.. | - || PDF | 25 50 44 46 | %PDF | %%EOF || ELF | 7F 45 4C 46 | .ELF | (Linux Executable) || MZ/PE| 4D 5A | MZ | (Windows Executable) |Commands:# 1. Cek tipe MIME dan deskripsi
file -b --mime-type target_file

# 2. Lihat header Hex (Head)
xxd target_file | head -n 10

# 3. Lihat footer Hex (Tail) - Penting untuk cek appended data
xxd target_file | tail -n 10

# 4. Hitung Hash (Untuk integritas bukti)
sha256sum target_file
2.2 Advanced String AnalysisMencari teks yang dapat dibaca manusia (ASCII/Unicode) di dalam binary sampah.# Basic string search (min 6 chars)
strings -n 6 target_file | less

# Mencari string dengan encoding Little Endian (Windows Unicode)
strings -e l target_file | grep "flag"

# Mencari format spesifik (misal flag format: picoCTF{...})
strings target_file | grep -iE "flag|pass|user|key|{.*}"

# TOOL REKOMENDASI: FLOSS (FireEye Labs Obfuscated String Solver)
# Jauh lebih kuat dari 'strings' biasa, bisa mendeteksi string yang di-stack di memori.
floss target_file
2.3 Entropy & Embedded Files DetectionMendeteksi apakah ada file di dalam file (Matryoshka).# 1. Analisis Entropy (Grafik visual)
binwalk -E target_file
# Jika grafik naik tajam menjadi datar (high entropy) di tengah, ada data terkompresi/enkripsi.

# 2. Signature Scan & Auto Extraction
# -M: Matryoshka (recursive), -e: extract
binwalk -Me target_file --run-as=root

# 3. Jika binwalk gagal, gunakan Foremost (File Carving)
# Foremost mengabaikan filesystem dan mencari header/footer raw.
foremost -i target_file -t all -o output_folder
🖼️ III. Deep Dive: Image SteganographyGambar adalah wadah paling umum untuk menyembunyikan data.3.1 Metadata & Structural Integrity# Cek EXIF lengkap
exiftool target_file

# Cek integritas PNG (CRC errors seringkali petunjuk stego manual)
pngcheck -vtp7f target.png
# Output "CRC error" atau "Additional data after IEND" adalah Red Flag besar.
3.2 LSB (Least Significant Bit) AnalysisMenyembunyikan pesan di bit terakhir (paling tidak penting) dari nilai warna piksel. Perubahan warna tidak terlihat mata manusia.Tools: zsteg (Linux CLI) & StegSolve (Java GUI).# Zsteg: "Swiss army knife" untuk PNG/BMP
zsteg -a target.png

# Opsi spesifik zsteg (mencoba semua kombinasi order)
zsteg -a --all target.png
Jika menggunakan StegSolve:Buka gambar.Gunakan panah kiri/kanan untuk geser filter (Red plane 0, Blue plane 0, dll).Cari pola noise yang tidak wajar atau teks tersembunyi.3.3 Steganografi Berbasis PassphraseTool ini menyisipkan data terenkripsi ke dalam gambar. Tanpa password, terlihat seperti noise acak.# 1. Coba ekstrak tanpa password (kosong)
steghide extract -sf target.jpg

# 2. Brute-force password Steghide menggunakan wordlist (rockyou.txt)
stegseek target.jpg /usr/share/wordlists/rockyou.txt
# Stegseek sangat cepat (jutaan pass/detik).
3.4 Teknik LainConcatenated Files: cat image.jpg archive.zip > image_stego.jpg. Solusi: binwalk atau unzip.Thumbnail Cache: Kadang gambar asli diedit/dicrop, tapi thumbnail EXIF masih menyimpan gambar original.🎵 IV. Deep Dive: Audio ForensicsAudio dianalisis dalam domain waktu (Waveform) dan domain frekuensi (Spectrogram).4.1 Visual AnalysisGunakan Audacity atau Sonic Visualiser.Waveform: Lihat bentuk gelombang. Jika ada blok kotak sempurna, itu data digital.Spectrogram: (Shift+M di Audacity). Ubah view ke Spectrogram. Seringkali teks "ditulis" menggunakan frekuensi suara.4.2 Hidden Channels & ModulationLSB Audio: Mirip image stego, menyembunyikan data di bit terkecil amplitudo.Dual Channel: Kanal Kiri (L) berisi musik, Kanal Kanan (R) berisi data morse/SSTV. Split stereo track menjadi mono.Reverse Audio: Mainkan lagu secara terbalik.CLI Tools:# Cek info file
soxi target.wav

# Buat spectrogram via CLI (cepat)
sox target.wav -n spectrogram

# Decode SSTV (Slow Scan TV) -> Audio to Image
# Gunakan: RX-SSTV (Windows) atau qsstv (Linux)
📽️ V. Deep Dive: Video ForensicsVideo adalah kontainer (MP4, MKV, AVI) yang membungkus stream Video, Audio, dan Subtitle.# 1. Inspeksi Stream detail
ffprobe target.mp4

# 2. Ekstrak Frame Spesifik
# Stego sering disisipkan di frame ke-X
ffmpeg -i target.mp4 -vf "select=eq(n\,100)" -vframes 1 frame_100.png

# 3. Ekstrak Audio saja
ffmpeg -i target.mp4 -vn -acodec copy audio_track.aac

# 4. Cari Subtitle tersembunyi
# Kadang flag ada di file .srt yang di-mux ke dalam video
ffmpeg -i target.mp4 -map 0:s:0 subs.srt
📄 VI. Deep Dive: Document (PDF & Office)Dokumen modern adalah struktur kompleks yang bisa menjalankan kode (JavaScript/VBA).6.1 PDF AnalysisPDF memiliki struktur pohon objek.# Statistik struktur PDF
pdfid target.pdf

# Analisis mendalam objek & stream (Cari /JS, /JavaScript, /OpenAction)
pdf-parser.py --stats target.pdf

# Cari stream yang mengandung kata kunci, lalu dekompresi (-f) dan dump (-d)
pdf-parser.py -s "flag" -f -d dumped_data.txt target.pdf

# Ekstrak attachment embedded
pdfdetach -saveall target.pdf
6.2 Microsoft Office (OLE & XML)Format Lama (.doc, .xls): Format biner OLE.Format Baru (.docx, .xlsx): XML dalam ZIP.# 1. Cek Macro Berbahaya (VBA)
olevba target.doc
# Perhatikan fungsi 'AutoOpen', 'Shell', 'Execute'.

# 2. Manual Unzip (Untuk .docx/.xlsx)
cp target.docx target.zip
unzip target.zip
# Cek folder: word/media/ (gambar tersembunyi), word/document.xml (teks tersembunyi)
💾 VII. Deep Dive: Memory Forensics (RAM)Analisis volatil memori untuk mencari proses malware, password di clipboard, atau koneksi jaringan.Tools: Volatility 3 (Python 3) atau Volatility 2 (Python 2).Workflow Volatility 2:# 1. Identifikasi Profile OS
volatility -f mem.raw imageinfo

# 2. List Proses (Cari yang aneh: svchost.exe parent-nya salah, dll)
volatility -f mem.raw --profile=Win7SP1x64 pslist

# 3. Environment Variables (Sering ada flag diset di env)
volatility -f mem.raw --profile=... envars

# 4. Command History (cmd.exe history)
volatility -f mem.raw --profile=... cmdscan
volatility -f mem.raw --profile=... consoles

# 5. Dump File dari Memori
volatility -f mem.raw --profile=... dumpfiles -n "secret.txt" -D output/
🌐 VIII. Deep Dive: Network (PCAP)Analisis paket jaringan menggunakan Wireshark dan TShark.8.1 Wireshark Filters (Cheat Sheet)http.request.method == POST (Cari data yang dikirim user: login, upload).frame contains "flag" (Cari string di seluruh raw packet).tcp.stream eq 0 (Ikuti percakapan lengkap sesi pertama).ip.src == 192.168.1.5 && ip.dst == 10.0.0.1 (Filter percakapan spesifik).8.2 File Extraction from PCAP# Wireshark GUI:
# File -> Export Objects -> HTTP / SMB / FTP

# CLI (Network Miner atau Tshark):
tshark -r traffic.pcap --export-objects "http,dest_dir"
8.3 TLS DecryptionJika Anda menemukan file ssl_key.log atau sertifikat RSA privat di dalam challenge:Wireshark: Edit -> Preferences -> Protocols -> TLS.(Pre-Master-Secret log filename): Masukkan path ke key.log.Traffic HTTPS akan terbuka menjadi HTTP biasa.🛠️ IX. Advanced Repair & Obfuscation Handling9.1 Header Repair (Manual Hex Editing)Skenario: file command bilang "data", tapi Anda tahu itu PNG. Header rusak.Buka hex editor: ghex target_file atau hexeditor target_file.Lihat 8 byte pertama. Apakah acak?Cari referensi header PNG: 89 50 4E 47 0D 0A 1A 0A.Timpa byte yang rusak dengan byte yang benar.Simpan dan cek ulang.9.2 XOR Brute ForceTeknik obfuskasi paling klasik. Setiap byte di-XOR dengan kunci K.Pendeteksian:File isinya karakter aneh tapi berulang.Banyak byte 00 (null) di file asli akan berubah menjadi nilai Key di file ter-XOR (karena 00 XOR K = K).Solusi:# Gunakan xortool untuk analisis panjang kunci & karakter paling mungkin
xortool -c 20 cipher_file

# Brute force 1-byte key bash script
for i in {0..255}; do
    printf "\\x$(printf %x $i)" > key.bin
    # Gunakan tool xor sistem atau script python
    python3 -c "import sys; k=int(sys.argv[1]); data=open('cipher','rb').read(); sys.stdout.buffer.write(bytes([b^k for b in data]))" $i > output_$i
done
9.3 Custom Encoding IdentificationGunakan CyberChef (Magic Wand feature).Base64: Karakter A-Z, a-z, 0-9, +, / dan diakhiri =.Base32: Huruf kapital A-Z dan angka 2-7, diakhiri =.Hex: Hanya 0-9 dan A-F.Rot13: Format teks biasa tapi tidak terbaca.📝 X. Laporan & DokumentasiTidak ada gunanya menemukan flag jika Anda tidak bisa menjelaskan caranya.Template Laporan Mini:Deskripsi Soal: Apa petunjuk awalnya?Identifikasi: Output file, binwalk, hash file.Langkah Analisis:"Saya menemukan anomali pada chunk PNG...""Saya mengekstrak data menggunakan..."Payload/Script: Sertakan one-liner atau script python yang dipakai.Flag: CTF{th1s_1s_th3_fl4g}.
