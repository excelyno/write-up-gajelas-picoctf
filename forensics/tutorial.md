prinsip dasar (mental model)
1. segala sesuatu adalah data
jika tidak terlihat berarti tersembunyi: kompresi, encoding , stego, metadata dan fragment
2. jangan berasumsi 
validasi setiap dugaan (magic bytes, ukuran file , header dan struktur)
3. bekerja bertahap
triage > identifikasi > ekstraksi > analisis > korelasi > validasi
4. otomatisasi sebanyak mungkin (script kecil untuk repetisi)
5. log semua langkah
seringkali flag muncul ketika meninjau ulang

---
1. Triage awal (wajib dilakukan semua kategori)

selalu lakukan analisis ini sebelum menyentuh analisis spesifik:
1.1 identifikasi file

file nama_file
exiftool nama_file
strings -n 6 nama_file | less
xxd nama_file | head
binwalk -Me nama_file

cek :
magicbytes cocok dengan ekstensi ?
ada embedded files(zip png atau tar dll )
ada path domain kunci atau hint dalam string?


1.2 cek kompresi atau archive tersembunyi

binwalk -e nama_file
foremost nama_file
scalpel nama_file
7z x nama_file

jika gagal - mungkin :
headers rusak -> kita lakukan perbaikan manual di hex editor
xor/simple obfuscation

1.2 metadata

exiftool *
exiv2 nama_file
pdfinfo file.pdf

cari
gps
creator
history
idden revisions (office atau pdf)

1.4 encoding umum

coba decode ke 
base64
base32
hex
rot13
url encode

bisa gunakan cyberchef
xxd -r 
dan base64 -d

---

2. Analisis spesifik pertipe file

-
A. image (PNG/JPG/BMP)
checklist :
metadata (kamera, editor)
data tersembunyi (stego / appended zip)
lsb steganography
duplicate chunks (png ihdr , iend)

steghide extract -sf img.jpg
zsteg img.png
pngcheck -v file.png
strings file.png | grep pico

jika tidak ada hasil -> cek color channels, histogram atau pesan di QR/ noise

-
B. audio (WAV/MP3)
cari 
morse
sstv
spectrogram message
lsb audio

tools 
audacity
sox file.wav -n spectrogram

tambahkan 
Reverse 
Ubah ke Mono
dan turunkan speednya

-
C. Video
subtitle tersembunyi
frame khusus
audio channel tersembunyi

tools 
ffmpeg -i video.mp4
ffmpeg -i video.mp4 -map 0:v frame_%04d.png

-
D. PDF / Office
hidden objects 
layers
attachments
Js tersembunyi


tools nya 
pdfdetach -saveall file.pdf
strings file.pdf | grep JS
oletools

-
E. Disk image / filesystem
bisa langsung mount -> cari timeline ,deleted files

tools nya ada beberapa 
mmls disk.img
fls -r disk.img
tsk_recover disk.img recovered/
autopsy

-
F. Memory (RAM)
cari 
proses mencurigakan
comand history
dan credentials

tools nya seperti 
volatility -f mem.img imageinfo
volatility -f mem.img pslist
volatility -f mem.img filescan

-
G. Network (PCAP)
urutan:
1. Rekonstruksi sesi HTTP
2. Cek credentials, upload
3. Ekstract files

kita gunakan tools wire shark 
wireshark
tshark -r file.pcap
tcpflow -r file.pcap


filter penting :
http
tcp.stream eq X
frame contains "flag"

---
3. hard? which hard it is?
-
1. file header repair
kita bisa buka hex terus kita repair ulang headernya
xxd file > hex.txt
bandinggkan dengan signature asli (misalnya png seprti apa)

-
2. xor / one bytes obfuscation
for i in {0..255}; do
  xorfile file $i > out$i
done

-
3. fragment reassembly
gunakan 
binwalk 
foremost 
manual join dengan offset

-
4. stego tingkat lanjut
outguess
f5
deepsteg patterns
pallette png stego


rangkuman eksekusi 
file 
strings | grep pico
binwalk -Me
exiftool
bukan di hex, cek header / tail
coba extract : 7z x, foremost, scalpel
cek encoding cyberchef
gunakan tools khusus sesuai denga tipenya
mau itu image, audi pd pcap dan memory
jika buntu
pikirkan compressed? encoded? xor? stego? corrupted header?


