FROM apache/airflow:2.9.2-python3.10

USER root
RUN apt-get update && apt-get install -y gcc g++ libpq-dev

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
