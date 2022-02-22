from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from utils import db, parse_pet
from datetime import timedelta
import os


DAG_ID = os.path.basename(__file__).replace('.pyc', '').replace('.py', '')
CONN_ID = 'airflow_test'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False
}


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='5 1 * * *' # https://crontab.guru/
) as dag:
    #TODO exchange name value, task_id, op_kwargs > df, table_name
    load_pet = PythonOperator(
        task_id='load_pet',
        python_callable=db.load_data_to_db,
        op_kwargs={
            'connector': CONN_ID,
            'df': parse_pet.get_df_pet(),
            'table_name': 'pet',
        }
    )