# Automation-System-UTS
# Online Book Catalog Organizer & Scraper

Aplikasi otomatisasi berbasis Python untuk mengumpulkan, menyaring, mengorganisasi, dan membackup data katalog buku dari web secara otomatis melalui Command Line Interface (CLI). Tugas Ujian Tengah Semester (UTS) Mata Kuliah **Automation Systems**, Program Studi Teknik Informatika, Universitas Pelita Bangsa.

## Anggota Kelompok
1. Muhammad Tafzil Rimzal — 312310529

Proyek ini dikerjakan sendiri oleh Muhammad Tafzil Rimzal

---

## Fitur Utama & Integrasi Materi
- **Web Scraping (Chapter 13)**: Mengambil minimal 30 data buku dari `https://books.toscrape.com/` menggunakan `requests` dan `BeautifulSoup`.
- **Regular Expressions (Chapter 9)**: Menggunakan `re` untuk ekstraksi nilai harga numerik dan penyaringan judul berdasarkan kata kunci (`--keyword`).
- **File I/O (Chapter 10)**: Membaca dan menyimpan data mentah serta hasil terstruktur ke dalam format `.txt` dan `.csv`.
- **Organisasi File & Backup (Chapter 11)**: Pembuatan direktori otomatis via `pathlib` dan kompresi hasil ke dalam arsip `.zip`.
- **CLI & Error Handling (Chapter 12)**: Penggunaan `argparse` untuk argumen fleksibel serta penanganan kegagalan koneksi & data kosong.

---

## Cara Instalasi & Penggunaan

### 1. Instalasi Dependensi
Pastikan Python telah terinstal, lalu jalankan perintah berikut di terminal:
```bash
pip install -r requirements.txt
```

### 2. Cara Menjalankan Program
Gunakan argumen CLI sesuai kebutuhan:
```bash
python main.py --limit 30 --backup
```

### Penjelasan Argumen CLI:
- `--url`: Menentukan URL target web scraping (harus menggunakan HTTP atau HTTPS).
- `--keyword`: Kata kunci penyaringan judul buku (opsional).
- `--limit`: Jumlah maksimum data yang diambil; harus berupa bilangan bulat positif (default: 30).
- `--backup`: Bendera (flag) untuk mengaktifkan pembuatan backup `.zip` otomatis.

Output selalu disimpan di dalam folder proyek. File CSV menggunakan UTF-8 dengan BOM
agar karakter khusus dan simbol mata uang terbaca dengan benar di aplikasi spreadsheet.
Katalog HTML dapat dibuka melalui `output/index.html`. Harga di CSV tetap dalam GBP;
halaman katalog menampilkan konversi IDR menggunakan kurs acuan tetap dan mencantumkan
tanggal kurs. Kurs tersebut bukan kurs live.

### Laporan dan Demo
Laporan PDF final berada di `dokumentasi/laporan_uts.pdf`. Untuk membuat ulang laporan
setelah memperbarui CSV:
```bash
python dokumentasi/generate_report.py
```

Urutan presentasi dan poin demonstrasi tersedia di `dokumentasi/naskah_demo.txt`.
Naskah bukan pengganti video; rekam video demonstrasi secara terpisah sebelum pengumpulan.
Slide presentasi ringkas tersedia di `dokumentasi/presentasi/Presentasi_UTS_Automation_Systems_Final.pptx`,
dengan agenda 5 menit penjelasan, 7 menit demo, dan 3 menit tanya jawab.
Video demo ringkas tersedia di `dokumentasi/presentasi/Video_Demo_UTS_Automation_Systems.mp4`
(46 detik, ber-caption tanpa audio). Video tersebut merupakan preview alur aplikasi; demonstrasi
langsung tetap disiapkan sesuai prosedur presentasi dosen.

### Batasan Data
Sumber katalog latihan tidak menyediakan nama penulis pada kartu buku yang diambil.
Field kategori saat ini adalah klasifikasi harga `Premium`/`Standard` (ambang £30),
bukan kategori genre dari situs.

---

## Struktur Direktori Proyek
```text
UTS_Project_Kelompok_01/
│
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── raw_data.txt
├── output/
│   ├── hasil_scraping.csv
│   ├── laporan.txt
│   └── index.html
├── backup/
│   └── backup_data.zip
└── dokumentasi/
    ├── laporan_uts.pdf
    ├── generate_report.py
    └── naskah_demo.txt
```
