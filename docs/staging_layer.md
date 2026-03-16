# Staging Layer

The **Staging Layer** is the **second layer in the data warehouse pipeline**.
Its purpose is to **clean, validate, and standardize raw data** before the data is loaded into the **Core Data Warehouse (DWH)** layer.

At this stage, data transformations are performed using **SQL in PostgreSQL** to ensure that the data structure and format are consistent and ready for analytical processing.

The processed data is stored in the **`staging` schema** and exported as CSV files as part of the pipeline output for traceability and validation.

---

# 📌 Purpose

The Staging Layer is responsible for:

* Extracting raw data from **raw tables** in PostgreSQL.
* Performing **data cleaning and initial transformations**.
* Standardizing column formats and data types.
* Loading the processed data into the **`staging` schema**.
* Exporting the staging output into **CSV files** for pipeline tracking.
* Preparing cleaned datasets for the **Core Data Warehouse Layer**.

This layer ensures that only **clean and standardized data** is forwarded to the next stage of the pipeline.

---

# 📂 File Structure

```text
pipeline/
└── run_staging.py

data/
└── staging/
    ├── query/
    │   └── customer_addresses.sql
    └── data/
        └── customer_addresses_YYYYMMDD.csv
```

Description:

* **run_staging.py**

  Main pipeline script responsible for:

  * reading SQL transformation files
  * executing transformations in PostgreSQL
  * loading results into `staging.customer_addresses`
  * exporting the staging data to CSV

* **customer_addresses.sql**

  SQL transformation script used to clean and process raw data.

---

# ⚙️ Pipeline Workflow

The staging pipeline runs the following steps:

### 1️⃣ Read SQL Transformation

The pipeline reads the SQL transformation script from:

```
data/staging/query/customer_addresses.sql
```

---

### 2️⃣ Inject Pipeline Parameter

The pipeline receives a **`file_date` parameter** which allows processing data per execution date.

Example:

```
20260301
```

This value is injected into the SQL query before execution.

---

### 3️⃣ Execute SQL Transformation

The SQL transformation is executed in PostgreSQL to perform:

* data cleaning
* format standardization
* column transformation
* data validation

---

### 4️⃣ Load into Staging Table

The processed data is loaded into the table:

```
staging.customer_addresses
```

This table contains cleaned and standardized records ready for the next pipeline layer.

---

### 5️⃣ Export Staging Snapshot

The staging result is exported as a CSV file for tracking and validation.

Output location:

```
data/staging/data/
```

Example output file:

```
customer_addresses_20260301.csv
```

---

# 🔄 Data Flow

```
Raw Tables (PostgreSQL)
        │
        ▼
SQL Transformation
        │
        ▼
Data Cleaning & Standardization
        │
        ▼
Load → staging.customer_addresses
        │
        ▼
Export Snapshot → data/staging/data/
        │
        ▼
Next Layer → Core Data Warehouse
```

---

# 🚀 How to Run

Execute the staging pipeline with the following command:

```bash
python pipeline/run_staging.py YYYYMMDD
```

Example:

```bash
python pipeline/run_staging.py 20260301
```

The pipeline will:

1. execute the SQL transformation
2. load cleaned data into `staging.customer_addresses`
3. export the staging result into a CSV file

Example output file:

```
data/staging/data/customer_addresses_20260301.csv
```

The console will display **pipeline logs and execution time**.

---

# 📝 Notes

* Ensure that **PostgreSQL is running** before executing the pipeline.
* SQL transformation logic is separated into `.sql` files for easier maintenance.
* The pipeline supports **date-based batch execution**.
* The staging pipeline can be orchestrated using **Apache Airflow DAGs** for automated scheduling.

---

# Next Step

After the data has been processed in the **Staging Layer**, it will be loaded into the **Core Data Warehouse Layer**.

In this layer, the cleaned data will be transformed into **dimension tables and fact tables** to support analytical queries and reporting.

See: ➡ **[DWH Layer](dwh_layer.md)**