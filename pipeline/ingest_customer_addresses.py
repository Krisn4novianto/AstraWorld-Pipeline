# ingestion/ingest_customer_addresses.py
import os
import shutil
import sys
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import config

# -----------------------------
# Config & Connection
# -----------------------------
def get_engine():
    password = quote_plus(config.DB_PASSWORD)
    engine = create_engine(
        f"postgresql+psycopg2://{config.DB_USER}:{password}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )
    return engine

# -----------------------------
# Ingest single CSV file
# -----------------------------
def ingest_file(file_date: str, engine, landing_folder="data/landing", raw_folder="data/raw"):
    filename = f"customer_addresses_{file_date}.csv"
    filepath = os.path.join(landing_folder, filename)

    if not os.path.exists(filepath):
        print(f"❌ File tidak ditemukan: {filepath}")
        return

    print(f"📄 Reading file: {filepath}")
    df = pd.read_csv(filepath)

    # Tambahin kolom file_date
    df["file_date"] = pd.to_datetime(file_date, format="%Y%m%d")

    print("🔍 Preview Data:")
    print(df.head())

    # Insert ke Postgres
    df.to_sql(
        name="customer_addresses",
        con=engine,
        if_exists="append",
        index=False
    )
    print("✅ Data berhasil dimasukkan ke Postgres.")

    # Pastikan folder RAW ada
    os.makedirs(raw_folder, exist_ok=True)

    # Pindahkan file ke RAW layer
    destination = os.path.join(raw_folder, filename)
    shutil.move(filepath, destination)
    print(f"📂 File dipindahkan ke RAW layer: {destination}")

# -----------------------------
# Main pipeline
# -----------------------------
def main():

    start_time = time.time()
    start_datetime = datetime.now()

    print("======================================")
    print("🚀 Starting Ingestion Pipeline")
    print(f"🕒 Start Time : {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================")

    if len(sys.argv) != 2:
        print("Usage: python ingest_customer_addresses.py YYYYMMDD")
        return

    file_date = sys.argv[1]

    # Validasi format tanggal
    try:
        pd.to_datetime(file_date, format="%Y%m%d")
    except ValueError:
        print("❌ Format tanggal salah. Gunakan YYYYMMDD.")
        return

    engine = get_engine()

    ingest_file(file_date, engine)

    end_time = time.time()
    end_datetime = datetime.now()

    duration = end_time - start_time

    print("======================================")
    print("✅ Pipeline Finished")
    print(f"🕒 End Time   : {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱ Duration   : {duration:.2f} seconds")
    print("======================================")

if __name__ == "__main__":
    main()
