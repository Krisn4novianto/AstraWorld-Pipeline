# Datamart Layer

**Datamart Layer** adalah **lapisan akhir dalam pipeline data warehouse** yang berfungsi untuk **menghasilkan laporan bisnis siap pakai** dari data di Staging Layer. Layer ini menyajikan informasi agregat yang dapat langsung digunakan oleh tim bisnis atau dashboard analitik.

---

## 📌 Tujuan

Datamart Layer bertugas untuk:

* Mengambil data dari Staging Layer dan melakukan agregasi.
* Membuat report bisnis siap pakai dan menyimpannya di Warehouse **schema datamart** serta menyalinnya ke folder `data/datamart/data/`.
* Menyediakan informasi untuk analisis, monitoring, dan pengambilan keputusan.

---

## 📂 Struktur File

```
pipeline/
└── run_datamart.py
```

* `run_datamart.py` → Script utama untuk generate report dari staging ke datamart.

---

## ⚙️ Alur Kerja

1. Ambil data dari **tabel staging** di Postgres.
2. Buat agregasi dan transformasi sesuai report:

   * `sales_summary` – total penjualan per `class` dan `model`
   * `service_priority` – jumlah service per customer
3. Simpan output ke folder `data/datamart/data/` dalam bentuk CSV.

> Flow diagram:
> `staging DB` → `aggregate & transform` → `save CSV datamart`

---

* **Report yang tersedia:**

| Report Name        | Deskripsi                               | Format  | Kategori                                                   |
| ------------------ | --------------------------------------- | ------- | ---------------------------------------------------------- |
| `sales_summary`    | Total penjualan per `class` dan `model` | YYYY-MM | LOW: 100–250 jt <br> MEDIUM: 250–400 jt <br> HIGH: >400 jt |
| `service_priority` | Jumlah service per customer             | YYYY    | LOW: <5x <br> MEDIUM: 5–10x <br> HIGH: >10x                |

---

## 🚀 Cara Menjalankan Report

### Menjalankan report `sales_summary`

```bash
python pipeline/run_datamart.py sales_summary
```

* Output: CSV report `sales_summary` di folder `data/datamart/data/`.
* Mengambil data dari staging dan mengelompokkan total penjualan per `class` dan `model`.

---

### Menjalankan report `service_priority`

```bash
python pipeline/run_datamart.py service_priority
```

* Output: CSV report `service_priority` di folder `data/datamart/data/`.
* Menghitung jumlah service per customer.


