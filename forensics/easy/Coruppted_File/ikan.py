import sys

def fix_jpeg(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Cari lokasi string "JFIF"
        # Struktur standar: [FF D8] [FF E0] [00 10] [J F I F]
        jfif_loc = data.find(b'JFIF')
        
        if jfif_loc == -1:
            print("Error: Tidak ditemukan marker JFIF. File mungkin bukan JPEG standar atau rusak parah.")
            return

        # Kita mundur 4 byte dari 'JFIF' untuk mendapatkan panjang (2 byte) dan marker APP0 (FF E0)
        # Offset yang kita harapkan untuk memulai data 'bersih' adalah 4 byte sebelum JFIF
        start_point = jfif_loc - 4
        
        if start_point < 0:
            print("Error: Struktur file terlalu pendek di awal.")
            return
            
        # Ambil data dari marker FF E0 sampai akhir
        # Ini membuang karakter sampah '\x' atau apapun yang ada di paling depan
        clean_data = data[start_point:]
        
        # Cek apakah data bersih dimulai dengan FF E0
        if not clean_data.startswith(b'\xff\xe0'):
            print("Warning: Marker sebelum JFIF bukan FF E0, tapi kita akan tetap mencoba memperbaikinya.")

        # Tambahkan Magic Bytes JPEG (FF D8) di paling depan
        fixed_data = b'\xff\xd8' + clean_data
        
        # Simpan sebagai file baru
        output_filename = 'flag.jpg'
        with open(output_filename, 'wb') as f:
            f.write(fixed_data)
            
        print(f"Sukses! File telah diperbaiki dan disimpan sebagai: {output_filename}")
        print("Silakan buka file 'flag.jpg' tersebut.")

    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Jalankan fungsi pada file.dat
fix_jpeg('file.dat')
