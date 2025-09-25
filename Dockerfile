FROM apache/airflow:2.11.0

USER root

# 安裝系統套件
RUN apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

