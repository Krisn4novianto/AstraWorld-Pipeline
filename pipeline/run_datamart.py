# pipeline/run_datamart.py
import os
import sys
import time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
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
# Read SQL from file
# -----------------------------
def read_sql_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found: {filepath}")
    with open(filepath, "r") as f:
        return f.read()

# -----------------------------
# Execute SQL (DDL/DML)
# -----------------------------
def execute_sql(engine, query: str):
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
    print("✅ SQL executed successfully in Postgres.")

# -----------------------------
# Export SELECT query to CSV
# -----------------------------
def export_to_csv(engine, select_query: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with engine.connect() as conn:
        df = pd.read_sql(text(select_query), conn)
        df.to_csv(output_path, index=False)
    print(f"✅ Data exported to CSV: {output_path}")

# -----------------------------
# Main Pipeline
# -----------------------------
def main():

    start_time = time.time()
    start_datetime = datetime.now()

    print("======================================")
    print("🚀 Starting Datamart Pipeline")
    print(f"🕒 Start Time : {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================")

    if len(sys.argv) != 2:
        print("Usage: python run_datamart.py <report_name>")
        print("Available reports: sales_summary, service_priority")
        sys.exit(1)

    report_name = sys.argv[1].lower()

    engine = get_engine()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Mapping report SQL
    report_sql_map = {
        "sales_summary": os.path.join(BASE_DIR, "data", "datamart", "query", "sales_summary.sql"),
        "service_priority": os.path.join(BASE_DIR, "data", "datamart", "query", "service_priority.sql")
    }

    if report_name not in report_sql_map:
        print(f"❌ Unknown report: {report_name}")
        sys.exit(1)

    sql_file = report_sql_map[report_name]

    output_csv = os.path.join(
        BASE_DIR,
        "data",
        "datamart",
        "data",
        f"{report_name}.csv"
    )

    # -----------------------------
    # 1️⃣ Run SQL
    # -----------------------------
    print(f"📄 Reading SQL file: {sql_file}")

    query = read_sql_file(sql_file)

    print(f"🚀 Running {report_name} query in Postgres...")
    execute_sql(engine, query)

    # -----------------------------
    # 2️⃣ Export CSV
    # -----------------------------
    select_query = f"SELECT * FROM datamart.{report_name};"

    print(f"📤 Exporting {report_name} data to CSV...")
    export_to_csv(engine, select_query, output_csv)

    # -----------------------------
    # End Pipeline
    # -----------------------------
    end_time = time.time()
    end_datetime = datetime.now()

    duration = end_time - start_time

    print("======================================")
    print(f"✅ Datamart Pipeline Finished ({report_name})")
    print(f"🕒 End Time   : {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱ Duration   : {duration:.2f} seconds")
    print("======================================")

if __name__ == "__main__":
    main()
