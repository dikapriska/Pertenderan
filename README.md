# Dashboard Tender LPSE

Aplikasi ini adalah **Dashboard Tender LPSE** yang menampilkan data tender dari LPSE (Layanan Pengadaan Secara Elektronik) di instansi pemerintah seluruh Indonesia dan memungkinkan pengguna untuk melakukan filter, pencarian, serta mengunduh data dalam format CSV, Excel dan PDF.

> DISCLAIMER:
>
> Penulis tidak terafiliasi dengan pengembang SPSE atau pemilik aplikasi SPSE. Aplikasi ini dikembangkan dengan tujuan akademis, bentuk pengawasan oleh masyarakat, dan membantu pengusaha untuk mempermudah otomasi perolehan informasi pengadaan dari pemerintah.
>
> Penggunaan yang tidak wajar dan mengganggu sebagian atau seluruh fungsi aplikasi SPSE pada satuan kerja menjadi tanggung jawab masing-masing pengguna.
>
> Jadi, gunakanlah aplikasi ini dengan bijak dan secukupnya.

## Fitur Utama

Aplikasi ini memiliki beberapa fitur penting, antara lain:

- **Filter Berdasarkan Kategori dan Instansi**: Pengguna dapat memilih instansi dan kategori tender yang ingin ditampilkan.
- **Pencarian Berdasarkan Nama Paket**: Pengguna dapat mencari nama paket tender yang relevan dengan memasukkan kata kunci.
- **Pengunduhan Data**: Pengguna dapat mengunduh data tender dalam format **CSV** atau **Excel**.
- **Export to PDF**: Pengguna dapat mengonversi tampilan tabel ke format PDF.

## Persyaratan

Sebelum menjalankan aplikasi, pastikan Anda sudah menginstal salah satu dependensi berikut:

- Python &gt;= 3.10
- Docker (jika ingin menjalankan aplikasi di dalam container Docker)

## Instalasi

### Instalasi di Lokal

1. **Clone Repository**

   Pertama, clone repository ini ke komputer lokal Anda:

   ```bash
   git clone https://github.com/dikapriska/Pertenderan
   cd Pertenderan
   ```

2. **Buat Virtual Environment dan Install Dependencies**

   Disarankan untuk menggunakan virtual environment untuk menghindari konflik dependensi.

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Untuk Linux/Mac
   venv\Scripts\activate      # Untuk Windows
   ```

   Kemudian, install semua dependensi yang diperlukan:

   ```bash
   pip install -r app/requirements.txt
   ```

3. **Siapkan File Konfigurasi** `.env`

   Buat file `.env` di root direktori **app** dan tambahkan konfigurasi berikut:

   ```
   URL_LPSE=<URL-API-LPSE>
   URL_TENDER=<URL-API-TENDER>
   ```

4. **Jalankan Aplikasi**

   Setelah dependensi terinstal dan file konfigurasi selesai, Anda dapat menjalankan aplikasi dengan perintah:

   ```bash
   streamlit run app/app.py
   ```

   Aplikasi akan berjalan di `http://localhost:8501`.

### Instalasi Menggunakan Docker

Jika Anda ingin menjalankan aplikasi di dalam Docker, Anda bisa mengikuti langkah-langkah berikut.

1. **Siapkan File Konfigurasi** `.env`

   Buat file `.env` di root direktori proyek Anda dan tambahkan konfigurasi berikut:

   ```
   URL_LPSE=<URL-API-LPSE>
   URL_TENDER=<URL-API-TENDER>
   ```

2. **Bangun Docker Image**

   ```bash
   docker build -t app-lpse .
   ```

3. **Jalankan Docker Container**

   Setelah image selesai dibangun, jalankan container dengan perintah:

   ```bash
   docker run -p 8501:8501 --env-file .env app-lpse
   ```

   Aplikasi akan dapat diakses di `http://localhost:8501`.

### Instalasi Menggunakan Docker Compose

Jika Anda ingin menjalankan aplikasi menggunakan docker compose, Anda bisa mengikuti langkah-langkah berikut.

1. **Siapkan File Konfigurasi** `.env`

   Buat file `.env` di root direktori proyek Anda dan tambahkan konfigurasi berikut:

   ```
   URL_LPSE=<URL-API-LPSE>
   URL_TENDER=<URL-API-TENDER>
   ```

2. **Jalankan Docker Compose**

   ```bash
   docker compose up --build -d
   ```

   Aplikasi akan dapat diakses di `http://localhost:7000`.

## Penggunaan

Setelah aplikasi dijalankan, Anda dapat menggunakan fitur-fitur berikut:

1. **Pilih LPSE dan Tahun**

   Pilih LPSE dan tahun tender yang ingin Anda lihat.

2. **Filter Berdasarkan Kategori dan Instansi**

   Gunakan dropdown untuk memfilter tender berdasarkan kategori dan instansi. Tersedia opsi "Semua" untuk menampilkan semua data.

3. **Pencarian Berdasarkan Nama Paket**

   Gunakan search bar untuk mencari nama paket tender yang sesuai.

4. **Unduh Data**

   Anda dapat mengunduh data dalam format CSV atau Excel dengan tombol unduh yang tersedia.

5. **Ekspor ke PDF**

   Pilih tombol "Ekspor ke PDF" untuk mengonversi tampilan tabel saat ini menjadi file PDF yang rapi.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan buka issue atau buat pull request. Kami sangat menghargai kontribusi Anda!

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](https://mit-license.org).

### Penjelasan:

- **Fitur Utama**: Menyebutkan semua fitur yang ada di aplikasi Anda, seperti filter, pencarian, download CSV atau Excel, dan eksport PDF.
- **Instalasi**: Menyediakan instruksi untuk instalasi baik di lokal (menggunakan virtual environment) maupun menggunakan Docker.
- **Penggunaan**: Memberikan panduan cara menggunakan aplikasi setelah dijalankan.
- **Kontribusi**: Mengundang orang lain untuk berkontribusi pada proyek ini jika mereka tertarik.