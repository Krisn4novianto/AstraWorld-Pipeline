FROM apache/airflow:2.7.1-python3.11

USER root
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
USER airflow