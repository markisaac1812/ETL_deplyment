FROM apache/airflow:3.2.2
COPY requirements.txt .
RUN pip install -r requirements.txt