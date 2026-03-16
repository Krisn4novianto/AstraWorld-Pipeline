# Core Data Warehouse Layer

**Core Data Warehouse (DWH) Layer** adalah **lapisan ketiga dalam pipeline data warehouse** yang berfungsi untuk **membangun model data analitis** menggunakan struktur **fact table dan dimension table**.

Pada layer ini, data yang sudah dibersihkan dari **Staging Layer** akan ditransformasikan lebih lanjut untuk membentuk **Star Schema**, sehingga data dapat dianalisis secara efisien dan konsisten.

Transformasi dilakukan menggunakan **SQL di PostgreSQL**.

---

# 📌 Tujuan

Core Data Warehouse Layer bertugas untuk:

* Mengambil data yang sudah dibersihkan dari **schema `staging`**.
* Membentuk **dimension table** yang menyimpan atribut deskriptif.
* Membentuk **fact table** yang menyimpan data transaksi atau metrik bisnis.
* Mengorganisasi data dalam struktur **Star Schema**.
* Menyediakan **single source of truth** untuk analisis data sebelum digunakan pada datamart.

Layer ini menjadi **sumber utama data analitis** yang digunakan oleh **Datamart Layer**.

---

# 📂 Struktur File

```
pipeline/
└── run_dwh.py
```

Keterangan:

* **run_dwh.py**

Script utama yang bertugas untuk:

* membaca file SQL transformasi untuk dimension dan fact table
* menjalankan query di PostgreSQL
* memuat data ke tabel di schema `dwh`

SQL transformasi disimpan di:

```
data/core/query/
```

Contoh file SQL:

```
data/core/query/load_dim_customer.sql
data/core/query/load_dim_vehicle.sql
data/core/query/load_dim_date.sql
data/core/query/load_fact_sales.sql
```

---

# 🗄 Struktur Tabel Data Warehouse

Schema `dwh` menggunakan **Star Schema** yang terdiri dari:

### Dimension Tables

Tabel yang menyimpan **atribut deskriptif** untuk analisis.

Berikut adalah skema tabelnya:

```
dwh.dim_customer
dwh.dim_vehicle
dwh.dim_date
```

Berikut adalah struktur tabelnya:

```
dim_customer
```

| customer_key | customer_id | customer_name | city | state |
| ------------ | ----------- | ------------- | ---- | ----- |

---

### Fact Tables

Tabel yang menyimpan **data transaksi atau metrik bisnis**.

Berikut adalah tabelnya:

```
dwh.fact_sales
dwh.fact_after_sales
```

Berikut adalah struktur tabelnya:

```
fact_sales
```

| sales_key | customer_key | vehicle_key | date_key | amount |
| --------- | ------------ | ----------- | -------- | ------ |

Fact table biasanya memiliki **foreign key ke dimension table**.

---

# ⚙️ Alur Kerja

Proses pada Core Data Warehouse Layer berjalan sebagai berikut:

1️⃣ Pipeline membaca file SQL transformasi dari folder:

```
data/core/query/
```

2️⃣ Parameter `file_date` dimasukkan ke dalam query untuk memproses data per tanggal.

3️⃣ Query SQL dijalankan di PostgreSQL untuk:

* membentuk dimension table
* mengisi fact table dari data staging

4️⃣ Data dimuat ke tabel berikut:

```
dwh.dim_customer
dwh.dim_vehicle
dwh.dim_date
dwh.fact_sales
```

5️⃣ Data warehouse siap digunakan oleh **Datamart Layer** untuk membuat laporan bisnis.

---

# 🔄 Flow Diagram

```
Staging Tables
(staging.customer_addresses, staging.sales)
        │
        ▼
Read SQL Transformation
        │
        ▼
Build Dimension Tables
        │
        ▼
Build Fact Tables
        │
        ▼
Load → dwh schema
```

---

# 🚀 Cara Menjalankan

Jalankan pipeline menggunakan command berikut:

```bash
python pipeline/run_dwh.py
```

Contoh:

```bash
python pipeline/run_dwh.py 20260301
```

Pipeline akan:

* memproses data dari schema `staging`
* memuat dimension dan fact table di schema `dwh`
* menyiapkan data warehouse untuk analisis.

---

# 📝 Catatan

* Schema `dwh` menggunakan **Star Schema** untuk performa analisis yang lebih baik.
* Dimension table biasanya berisi **data master atau atribut deskriptif**.
* Fact table berisi **data transaksi atau metrik bisnis**.
* Transformasi disimpan dalam file `.sql` terpisah untuk memudahkan maintenance.
* Pipeline ini dapat dijalankan **per batch berdasarkan tanggal data**.

---

# Next Step

Setelah data dimuat ke **Core Data Warehouse Layer**, data akan digunakan oleh **Datamart Layer** untuk membuat agregasi bisnis dan dataset yang siap digunakan oleh dashboard atau laporan analitik.

See: ➡ **[Datamart Layer](datamart_layer.md)**
