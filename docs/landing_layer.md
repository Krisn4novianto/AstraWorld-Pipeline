# Landing Layer

**Landing Layer** adalah **lapisan pertama dalam pipeline data warehouse** yang berfungsi sebagai titik masuk data mentah dari sumber eksternal. Layer ini memastikan data **disimpan dalam bentuk aslinya (raw)** sebelum dilakukan transformasi lebih lanjut, sehingga setiap tahap downstream memiliki **sumber data yang konsisten dan dapat ditelusuri**.

---

# 📌 Tujuan

Landing Layer bertujuan untuk:

* Mengambil data mentah (**raw CSV**) dari sumber eksternal.
* Melakukan **validasi dasar** terhadap file input.
* Memasukkan data ke **database raw layer**.
* Memindahkan file yang sudah diproses ke folder `data/raw/` sebagai **arsip raw data**.
* Menjaga **traceability data** sehingga proses pipeline dapat diaudit atau diulang jika diperlukan.

---

# 📂 Struktur File

```
ingestion/
└── ingest_customer_addresses.py
```

Keterangan:

* **ingest_customer_addresses.py**
  Script utama yang bertugas untuk:

  * membaca file CSV dari folder `data/landing/`
  * menambahkan metadata `file_date`
  * memasukkan data ke tabel `customer_addresses` di PostgreSQL
  * memindahkan file yang sudah diproses ke folder `data/raw/`

---

# ⚙️ Alur Kerja

Proses pada Landing Layer berjalan sebagai berikut:

1️⃣ Pipeline membaca file CSV dari folder:

```
data/landing/
```

2️⃣ Sistem melakukan validasi dasar:

* memastikan file tersedia
* memastikan format tanggal valid
* memastikan file dapat dibaca sebagai CSV

3️⃣ Data dibaca menggunakan **Pandas DataFrame**.

4️⃣ Pipeline menambahkan kolom metadata:

```
file_date
```

yang menunjukkan tanggal data tersebut diproses.

5️⃣ Data dimasukkan ke database PostgreSQL:

```
public.customer_addresses
```

menggunakan metode **append insert**.

6️⃣ Setelah proses ingest berhasil, file CSV dipindahkan dari:

```
data/landing/
```

ke:

```
data/raw/
```

sebagai **arsip data mentah yang telah diproses**.

---

# 🔄 Flow Diagram

```
External CSV
      │
      ▼
data/landing/
      │
      ▼
Read CSV (Pandas)
      │
      ▼
Add Metadata (file_date)
      │
      ▼
Insert to PostgreSQL (Raw Table)
      │
      ▼
Move file → data/raw/
```

---

# 🚀 Cara Menjalankan

Jalankan pipeline menggunakan command berikut:

```bash
python pipeline/ingest_customer_addresses.py YYYYMMDD
```

Contoh:

```bash
python pipeline/ingest_customer_addresses.py 20260301
```

Pipeline akan:

* membaca file

```
data/landing/customer_addresses_20260301.csv
```

* memasukkan data ke PostgreSQL
* memindahkan file ke:

```
data/raw/customer_addresses_20260301.csv
```

Console akan menampilkan **log proses ingest serta waktu eksekusi pipeline**.

---

# Next Step

Setelah data berhasil di-ingest ke **Raw Layer**, data akan diproses lebih lanjut pada tahap **Staging Layer** untuk melakukan proses pembersihan data, deduplikasi, dan transformasi awal sebelum digunakan dalam analisis.

See: ➡ **[Staging Layer](staging_layer.md)**


