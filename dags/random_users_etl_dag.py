from datetime import timedelta
import sys
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/scripts")  # Add the scripts directory to the Python path

from etl import run_etl

cairo_timezone = pendulum.timezone("Africa/Cairo")

default_args = {
	"owner": "airflow",
	"retries": 1,
	"retry_delay": timedelta(minutes=5),
}


with DAG(
	dag_id="random_users_daily_etl",
	default_args=default_args,
	description="Run the random users ETL every day at 8 PM Egypt time.",
	schedule="0 20 * * *",
	start_date=pendulum.datetime(2024, 1, 1, tz=cairo_timezone),
	catchup=False,
	tags=["etl", "random-users", "egypt-time"],
) as dag:
	run_random_users_etl = PythonOperator(
		task_id="run_random_users_etl",
		python_callable=run_etl,
	)