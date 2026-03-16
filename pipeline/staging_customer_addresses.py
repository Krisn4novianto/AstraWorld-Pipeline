import os
import sys
import time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import config


# --------------------------------
# Database Connection
# --------------------------------
def get_engine():
    password = quote_plus(config.DB_PASSWORD)

    engine = create_engine(
        f"postgresql+psycopg2://{config.DB_USER}:{password}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

    return engine


# --------------------------------
# Read SQL File
# --------------------------------
def read_sql_file(filepath: str) -> str:

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ SQL file not found: {filepath}")

    with open(filepath, "r") as f:
        return f.read()


# --------------------------------
# Execute SQL
# --------------------------------
def execute_sql(engine, query: str):

    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()


# --------------------------------
# Export Query Result to CSV
# --------------------------------
def export_to_csv(engine, query: str, output_path: str):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    df.to_csv(output_path, index=False)

    print(f"📁 CSV saved: {output_path}")


# --------------------------------
# Main Pipeline
# --------------------------------
def main():

    start_time = time.time()
    start_datetime = datetime.now()

    print("======================================")
    print("🚀 Starting Staging Pipeline")
    print(f"🕒 Start Time : {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================")

    # --------------------------------
    # Validate input argument
    # --------------------------------
    if len(sys.argv) != 2:
        print("Usage: python run_staging.py YYYYMMDD")
        sys.exit(1)

    file_date = sys.argv[1]

    try:
        pd.to_datetime(file_date, format="%Y%m%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYYMMDD")
        sys.exit(1)

    date_sql = f"{file_date[:4]}-{file_date[4:6]}-{file_date[6:]}"


    # --------------------------------
    # Database connection
    # --------------------------------
    engine = get_engine()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sql_file = os.path.join(
        BASE_DIR,
        "data",
        "staging",
        "query",
        "customer_addresses.sql"
    )

    print(f"📄 Loading SQL file: {sql_file}")

    query = read_sql_file(sql_file)

    query = query.replace("{{file_date}}", f"'{date_sql}'")


    # --------------------------------
    # Execute Staging Query
    # --------------------------------
    print(f"🚀 Executing staging query for {date_sql}")

    execute_sql(engine, query)

    print("✅ Staging table loaded successfully")


    # --------------------------------
    # Export to CSV
    # --------------------------------
    export_query = f"""
        SELECT *
        FROM staging.customer_addresses
        WHERE file_date = '{date_sql}'
    """

    output_csv = os.path.join(
        BASE_DIR,
        "data",
        "staging",
        "data",
        f"customer_addresses_{file_date}.csv"
    )

    print("📤 Exporting staging data to CSV...")

    export_to_csv(engine, export_query, output_csv)


    # --------------------------------
    # Pipeline End
    # --------------------------------
    end_time = time.time()
    end_datetime = datetime.now()

    duration = end_time - start_time

    print("======================================")
    print("✅ Staging Pipeline Finished")
    print(f"🕒 End Time   : {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱ Duration   : {duration:.2f} seconds")
    print("======================================")


if __name__ == "__main__":
    main()