import os
import sys
import time
from datetime import datetime
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import config


# -----------------------------
# Database Connection
# -----------------------------
def get_engine():
    password = quote_plus(config.DB_PASSWORD)

    engine = create_engine(
        f"postgresql+psycopg2://{config.DB_USER}:{password}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

    return engine


# -----------------------------
# Read SQL File
# -----------------------------
def read_sql_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found: {filepath}")

    with open(filepath, "r") as f:
        return f.read()


# -----------------------------
# Execute SQL
# -----------------------------
def execute_sql(engine, query):

    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()


# -----------------------------
# Main Pipeline
# -----------------------------
def main():

    start_time = time.time()
    start_datetime = datetime.now()

    print("======================================")
    print("🚀 Starting Core Data Warehouse Pipeline")
    print(f"🕒 Start Time : {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================")

    if len(sys.argv) != 2:
        print("Usage: python run_dwh.py YYYYMMDD")
        sys.exit(1)

    file_date = sys.argv[1]

    date_sql = f"{file_date[:4]}-{file_date[4:6]}-{file_date[6:]}"

    engine = get_engine()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    schema_dir = os.path.join(BASE_DIR, "dwh", "schema")
    query_dir = os.path.join(BASE_DIR, "dwh", "query")

    # -----------------------------
    # Schema SQL
    # -----------------------------
    schema_files = [
        "create_schema.sql",
        "dim_customer.sql",
        "dim_vehicle.sql",
        "dim_date.sql",
        "fact_sales.sql",
        "fact_after_sales.sql"
    ]

    # -----------------------------
    # Load SQL
    # -----------------------------
    load_files = [
        "load_dim_customer.sql",
        "load_dim_vehicle.sql",
        "load_dim_date.sql",
        "load_fact_sales.sql",
        "load_fact_after_sales.sql"
    ]

    # -----------------------------
    # Create Tables
    # -----------------------------
    print("📦 Creating DWH schema & tables...")

    for file in schema_files:

        path = os.path.join(schema_dir, file)

        print(f"   Running schema: {file}")

        query = read_sql_file(path)

        execute_sql(engine, query)

    # -----------------------------
    # Load Data
    # -----------------------------
    print("📥 Loading dimension & fact tables...")

    for file in load_files:

        path = os.path.join(query_dir, file)

        print(f"   Loading data: {file}")

        query = read_sql_file(path)

        query = query.replace("{{file_date}}", f"'{date_sql}'")

        execute_sql(engine, query)

    # -----------------------------
    # End Pipeline
    # -----------------------------
    end_time = time.time()
    end_datetime = datetime.now()

    duration = end_time - start_time

    print("======================================")
    print("✅ Core Data Warehouse Finished")
    print(f"🕒 End Time   : {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱ Duration   : {duration:.2f} seconds")
    print("======================================")


if __name__ == "__main__":
    main()