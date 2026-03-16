# Docker Local Setup

## 🎯 Tujuan

Menjalankan **seluruh environment pipeline secara lokal** menggunakan Docker agar:

* PostgreSQL siap sebagai **data warehouse**.
* Airflow siap sebagai **scheduler, executor, dan web UI**.
* Pipeline ETL (Landing → Staging → Datamart) bisa langsung dijalankan.
* Semua tim menggunakan **environment konsisten**.

---

## 🐳 Docker Compose

File utama: `docker-compose.yml`

Menjalankan container:

| Container           | Fungsi                       | Port |
| ------------------- | ---------------------------- | ---- |
| `postgres`          | Menyimpan warehouse database | 5432 |
| `airflow_webserver` | Web UI Airflow               | 8080 |
| `airflow_scheduler` | Menjadwalkan eksekusi DAG    | –    |
| `airflow_worker`    | Menjalankan task DAG         | –    |

### Jalankan Docker Compose

```bash
docker-compose up -d
```

* Gunakan `docker-compose ps` untuk melihat status container.
* Gunakan `docker-compose logs -f <container_name>` untuk melihat log real-time.

### Menghentikan Container

```bash
docker-compose down
```

---

## ⚙️ Environment & Konfigurasi

### 1️⃣ Folder Mapping

Pastikan folder berikut sudah ada di project root:

```text
data/raw/
data/staging/data/
data/datamart/data/
```

* Folder ini di-mount ke container Airflow/Postgres agar pipeline bisa membaca dan menulis file CSV.

### 2️⃣ Database Configuration

Sesuaikan `config.py` dengan environment Docker:

```python
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "astraworld"
```

> Jika menggunakan container network, `DB_HOST` bisa diganti dengan nama service Postgres di docker-compose, misal `postgres`.

### 3️⃣ Port Mapping

Pastikan port 5432 (Postgres) dan 8080 (Airflow) **tidak bentrok** dengan aplikasi lain di mesin lokal.

---

## ✅ Tips & Troubleshooting

* Airflow Web UI: [http://localhost:8080](http://localhost:8080)

  * Default login: `admin / admin`
* DAG pipeline otomatis muncul di UI setelah container berjalan.
* Untuk trigger manual, monitoring task, dan melihat logs, lihat [`docs/airflow.md`](docs/airflow.md)
* Jika ada container gagal start:

  1. Pastikan port tidak bentrok
  2. Pastikan folder data sudah ada
  3. Gunakan `docker-compose logs -f <container>` untuk debugging


