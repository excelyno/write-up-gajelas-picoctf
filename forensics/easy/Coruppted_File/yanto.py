# 1. Buka file yang rusak (mode 'rb' artinya baca biner/data mentah)
with open('file.dat', 'rb') as file_masuk:
    data_kotor = file_masuk.read()

# 2. Cari lokasi "JFIF" (Tanda pengenal file gambar)
# Kita cari di mana teks "JFIF" bersembunyi di dalam tumpukan data
posisi_jfif = data_kotor.find(b'JFIF')

# 3. Potong dan Ambil Data yang Berguna
# Aturan JPG: Data asli dimulai 4 langkah sebelum tulisan "JFIF".
# Jadi kita ambil data mulai dari posisi itu sampai habis.
data_potongan = data_kotor[posisi_jfif - 4 : ]

# 4. Tambahkan "Kepala" (Header) Baru
# Setiap JPG wajib diawali kode heksadesimal FF D8.
# Ini ibarat menempelkan stempel "INI ADALAH FOTO" di paling depan.
kepala_baru = b'\xff\xd8'
gambar_utuh = kepala_baru + data_potongan

# 5. Simpan jadi file gambar baru
with open('flag.jpg', 'wb') as file_keluar:
    file_keluar.write(gambar_utuh)

print("Berhasil! Silakan buka file 'flag.jpg'.")
