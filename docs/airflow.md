# ⚙️ Airflow Setup & Pipeline

## 🎯 Tujuan

Menjalankan **ETL pipeline harian** menggunakan **Apache Airflow DAG** untuk mengotomatisasi proses dari data mentah hingga siap untuk analisis bisnis.

Pipeline mencakup:

* Orkestrasi **Landing → Staging → Data Warehouse → Datamart**
* Scheduling otomatis harian
* Trigger manual
* Monitoring via Airflow UI
* Validasi setiap tahap sebelum lanjut ke proses berikutnya

DAG utama:

```
airflow/dags/dag_pipeline.py
```

---

## ⚠️ Prerequisites

> Apache Airflow **tidak support Windows secara native**
> Gunakan:

* ✅ **WSL2 (Ubuntu)** → recommended
* atau Docker

> Gunakan Python:

```
Python 3.13 ✅
```

---

## 🚀 Setup & Run Airflow (WSL2)

Panduan ini menjelaskan cara menjalankan **Airflow orchestration** untuk pipeline ini menggunakan **WSL2 + Python virtual environment**.

---

### 1️⃣ Prerequisites

Pastikan sudah terinstall:

* **WSL2**
* **Ubuntu (WSL)**
* **Python 3.10+**
* **pip**

Install WSL jika belum ada:

```bash
wsl --install
```

Masuk ke Ubuntu:

```bash
wsl -d Ubuntu
```

---

### 2️⃣ Clone Repository

Clone project ke komputer kamu.

```bash
git clone https://github.com/<your-repo>.git
```

Masuk ke folder project:

```bash
cd AstraWorld
```

Jika project berada di Windows path:

```bash
cd /mnt/c/Users/User/Downloads/AstraWorld
```

---

### 3️⃣ Verify Python Installation

Pastikan Python sudah tersedia di WSL.

```bash
python3 --version
```

Minimal:

```
Python 3.10+
```

Jika belum ada:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

---

### 4️⃣ Create Virtual Environment

Buat environment terpisah agar dependency project tidak bercampur dengan sistem.

```bash
python3 -m venv venv
```

Aktifkan virtual environment:

```bash
source venv/bin/activate
```

Jika ingin reset environment:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

---

### 5️⃣ Install Apache Airflow

Install Airflow dengan constraint yang sesuai dengan versi Python.

```bash
pip install "apache-airflow==2.9.3" \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2).txt"
```

Verifikasi instalasi:

```bash
airflow version
```

---

### 6️⃣ Configure AIRFLOW_HOME

Set folder Airflow agar berada di dalam project.

```bash
export AIRFLOW_HOME=$(pwd)/airflow
```

Struktur folder Airflow akan dibuat seperti ini:

```
AstraWorld
│
├── airflow
│   ├── dags
│   ├── logs
│   ├── plugins
│   └── airflow.db
```

Airflow akan membaca DAG dari folder:

```
$AIRFLOW_HOME/dags/
```

---
Gas, gue rapihin biar **lebih clean, profesional, dan jelas step-by-step** (biar enak dibaca recruiter juga) 👇

---

### 7️⃣ Initialize Airflow Database

Jalankan perintah berikut untuk inisialisasi database metadata Airflow:

```bash
airflow db migrate
```

---

### 8️⃣ Start Airflow

Jalankan Airflow dalam mode standalone:

```bash
airflow standalone
```

Perintah ini akan otomatis menjalankan:

* Webserver
* Scheduler
* Triggerer
* Inisialisasi database (jika belum)

> ⚠️ Setelah menjalankan perintah ini, **jangan tutup terminal** karena Airflow berjalan di sini.

---

## 🌐 Akses Airflow Web UI (WSL)

### ⚠️ Penting

Pada environment **WSL (Windows Subsystem for Linux)**, **jangan gunakan**:

```
http://localhost:8080
```


### 1. Buka terminal baru (WSL)

```bash
wsl -d Ubuntu
```

---

### 2. Masuk ke project

```bash
cd /mnt/c/Users/User/Downloads/AstraWorld
```

---

### 3. Ambil IP Address WSL

```bash
hostname -I
```

Contoh output:

```
172.26.181.10
```

---

### 4. Buka di browser

```
http://172.26.181.10:8080
```

---

## 🔐 Login Airflow

Saat menjalankan:

```bash
airflow standalone
```

Akan muncul informasi login seperti berikut:

```
Login with username: admin
password: xxxxxxxxx
```

Gunakan credential tersebut untuk login ke Airflow Web UI.

---

## 🌐 Menggunakan Airflow Web UI

Setelah berhasil login ke **Airflow Web UI**, langkah selanjutnya adalah **menjalankan dan memonitor pipeline**.

---

### 🔍 1. Masuk ke Menu DAGs

Pada halaman utama Airflow:

1. Klik menu **DAGs**
2. Akan muncul daftar pipeline yang tersedia
3. Cari DAG berikut:

```
daily_pipeline
```

---

### ▶️ 2. Aktifkan DAG

Sebelum menjalankan pipeline, DAG harus diaktifkan terlebih dahulu.

Langkah-langkah:

1. Klik **toggle switch** di sebelah kiri nama DAG
2. Pastikan status berubah menjadi **ON (aktif)**

⚠️ **Catatan:**
Jika DAG tidak diaktifkan, pipeline **tidak dapat dijalankan** baik secara manual maupun otomatis.

---

### 🚀 3. Trigger Pipeline (Manual Run)

Untuk menjalankan pipeline secara manual:

1. Klik tombol **▶ Trigger DAG** di pojok kanan atas
2. Airflow akan membuat **DAG Run baru**

---

### 📊 4. Monitoring Pipeline

Setelah pipeline dijalankan:

1. Klik nama DAG **`daily_pipeline`**
2. Buka salah satu tampilan berikut:

   * **Grid View**
   * **Graph View**

Di halaman ini Anda dapat melihat **status setiap task**.

#### Status Task

| Status     | Arti                           |
| ---------- | ------------------------------ |
| 🟩 Success | Task berhasil                  |
| 🟥 Failed  | Task mengalami error           |
| 🟨 Running | Task sedang berjalan           |
| ⬜ Queued   | Task menunggu untuk dijalankan |

---

### 🔗 5. Struktur Task Pipeline

Pipeline terdiri dari beberapa task yang berjalan **secara berurutan**:

| Task                          | Deskripsi                                                     |
| ----------------------------- | ------------------------------------------------------------- |
| **landing**                   | Mengambil data dari CSV dan memasukkannya ke **raw database** |
| **staging**                   | Melakukan **cleaning dan transformasi data**                  |
| **dwh_loading**               | Memuat data ke **Data Warehouse**                             |
| **datamart_sales_summary**    | Membuat agregasi data **penjualan**                           |
| **datamart_service_priority** | Membuat data **prioritas layanan/service**                    |

---

### 🧪 6. Debugging Jika Pipeline Gagal

Jika ada task berwarna **merah (Failed)**:

1. Klik task tersebut
2. Buka tab **Log**
3. Periksa detail error yang muncul

### Contoh Error Umum

* ❌ Koneksi database gagal
* ❌ File CSV tidak ditemukan
* ❌ Error pada script Python

---

### 🔁 7. Retry Task

Jika sebuah task gagal:

1. Klik task tersebut
2. Klik tombol **Clear**
3. Jalankan ulang DAG atau task tersebut

Airflow akan mencoba menjalankan task kembali.

---

### ⏱️ 8. Scheduling (Otomatis Harian)

DAG ini menggunakan schedule:

```
0 2 * * *
```

Artinya:

Pipeline akan berjalan **setiap hari pada pukul 02:00 UTC** secara otomatis.

---

### 📈 9. View Tambahan di Airflow

Airflow menyediakan beberapa tampilan untuk memonitor pipeline:

| View              | Fungsi                                        |
| ----------------- | --------------------------------------------- |
| **Grid View**     | Melihat status task (paling sering digunakan) |
| **Graph View**    | Menampilkan alur pipeline                     |
| **Gantt View**    | Melihat durasi setiap task                    |
| **Calendar View** | Melihat riwayat eksekusi pipeline             |


