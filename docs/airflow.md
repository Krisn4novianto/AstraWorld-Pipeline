# Airflow Setup & Pipeline

## 🎯 Tujuan

Menjalankan **ETL pipeline harian** menggunakan **Apache Airflow DAG** untuk mengotomatisasi proses pemrosesan data dari sumber mentah hingga siap digunakan untuk analisis bisnis.

Pipeline ini mencakup beberapa proses utama:

* Menjadwalkan pipeline otomatis setiap hari.
* Mengorkestrasi proses **Landing → Staging → Data Warehouse → Datamart**.
* Memungkinkan **trigger manual** untuk menjalankan pipeline kapan saja.
* Monitoring task pipeline melalui **Airflow UI**.
* Memastikan setiap proses berhasil sebelum melanjutkan ke tahap berikutnya.

DAG utama berada pada file:

```
airflow/dags/dag_pipeline.py
```

---

## ⚙️ Setup Airflow di Lokal

### 1️⃣ Install Apache Airflow (jika belum ada)

```bash id="0wn16f"
pip install apache-airflow
```

> Pastikan versi Python >= 3.13

### 2️⃣ Set Airflow Home Directory

```bash id="3pln2k"
export AIRFLOW_HOME=<path-to-project>/airflow
# Windows (PowerShell)
$env:AIRFLOW_HOME="<path-to-project>\airflow"
```

---

### 3️⃣ Inisialisasi Database Airflow

```bash id="9cxmkt"
airflow db init
```

> Airflow akan membuat **metadata database** dan folder struktur DAG, logs, plugins.

---

### 4️⃣ Start Airflow Standalone (Local)

```bash id="opk5mq"
airflow standalone
```

* Menjalankan sekaligus:

  * Scheduler
  * Webserver (UI)
  * Metadata database
* Web UI: [http://localhost:8080](http://localhost:8080)

  * Default credentials: `admin / admin`

> Untuk setup via Docker, lihat [`docs/docker.md`](docs/docker.md)

---

## ⏱ DAG Pipeline – AstraWorld

### 1️⃣ Alur ETL

```text
Landing (ingest_customer_addresses.py)
       ↓
Staging (staging_customer_addresses.py)
       ↓
Core DWH (run_dwh.py)
       ↓
Datamart (run_datamart.py)
       ├─ sales_summary
       └─ service_priority
```

Pipeline ini menjalankan proses berikut:

1. **Landing Layer**
   - Mengambil data CSV dari sumber eksternal
   - Memindahkan data ke folder `data/raw`

2. **Staging Layer**
   - Melakukan data cleaning
   - Transformasi awal
   - Load ke schema `staging`

3. **Core Data Warehouse**
   - Mengisi tabel **dimension dan fact**
   - Star schema pada schema `dwh`

4. **Datamart Layer**
   - Menghasilkan dataset analitik
   - Digunakan untuk reporting bisnis

### 2️⃣ Schedule

* Harian, jam 02:00
* Catchup: False (tidak mengejar tanggal terlewat)

> DAG otomatis mengeksekusi pipeline sesuai urutan di atas, termasuk logging setiap task.

---

## 🚀 Trigger DAG Manual

1. Buka Airflow UI: [http://localhost:8080](http://localhost:8080)
2. Cari DAG: `data_pipeline`
3. Klik **Enable DAG**
4. Klik **Trigger DAG** untuk eksekusi manual

---

## 📊 Monitoring & Logs

* Di Airflow UI, klik DAG → **Graph View / Tree View**
* Task status:

  * ✅ Success
  * ❌ Failed
  * ⏳ Running
* Klik task → **View Log** untuk detail error / info eksekusi

---

## ⚠️ Tips & Troubleshooting

* Pastikan folder data pipeline sudah ada:

```text
data/raw/
data/staging/data/
data/datamart/data/
```

* Jika DAG tidak muncul:

  * Pastikan DAG file berada di folder `airflow/dags/`
  * Restart Airflow scheduler / standalone

* Untuk pipeline via Docker: DAG akan otomatis muncul setelah container berjalan

* Gunakan logs untuk debugging task gagal atau cek dependencies