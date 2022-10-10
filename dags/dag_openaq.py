from airflow import DAG

from airflow.models.dagrun import DagRun

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

import boto3
from botocore import UNSIGNED
from botocore.client import Config

from datetime import date, datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"

s3bucket = "openaq-fetches"

postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

postgres_driver_jar = "/usr/local/spark/resources/jars/postgresql-9.4.1207.jar"

temp_path = "/usr/local/spark/resources/temp/"
first_execution = "/usr/local/spark/resources/first_execution.txt"

dag_id = "spark-openaq-module"
min_delta = 5

###############################################
# Callable functions
###############################################

def check_if_task_already_ran(dag_id: str):
    dag_runs = DagRun.find(dag_id=dag_id)
    if len(dag_runs) == 1:
        with open(first_execution, "w") as f:
            f.write(f"{dag_runs[0].start_date.strftime('%Y-%m-%d %H:%M:%S')}")

def get_key():
    with open(first_execution, "r") as f:
        first_date = datetime.strptime(str.rstrip(f.read()), "%Y-%m-%d %H:%M:%S")
        
        c = datetime.now() - first_date 
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', minutes)

    start_date = date(2017, 8, 11)
    end_date = start_date + timedelta(int(minutes/min_delta))
    
    print(end_date.strftime('%Y-%m-%d'))
    return f"{end_date.strftime('%Y-%m-%d')}.csv"

def download_from_s3(folder: str, bucket_name: str):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    key = get_key()
    with open(f"{temp_path}/{key}", "wb") as f:
        s3.download_fileobj(bucket_name, f"{folder}/{key}", f)

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) - timedelta(minutes=min_delta),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id=dag_id, 
    description="This DAG runs a pyspark app on openaq data.",
    default_args=default_args, 
    schedule_interval=timedelta(minutes=min_delta)
)

start = DummyOperator(task_id="start", dag=dag)

create_temp = BashOperator(   
    task_id="create_temp_dir",
    bash_command=f"mkdir -p {temp_path}",
    dag=dag
)

check_ran = PythonOperator(
    task_id="check_if_task_already_ran",
    python_callable=check_if_task_already_ran,
    op_kwargs={
        "dag_id": dag_id
    },
    dag=dag
)

download = PythonOperator(
    task_id="download_from_s3",
    python_callable=download_from_s3,
    op_kwargs={
        "folder": "daily",
        "bucket_name": s3bucket,
    },
    dag=dag
)

spark_job = SparkSubmitOperator(
    task_id="openaq_spark_job",
    application="/usr/local/spark/app/openaq_dag.py", 
    name="openaq-module",
    conn_id="spark_default",
    verbose=1,
    conf={
        "spark.master":spark_master
    },
    application_args=[temp_path, postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag
)

remove_temp = BashOperator(   
    task_id="remove_temp_dir",
    bash_command=f"rm -rf {temp_path}",
    dag=dag
)

end = DummyOperator(task_id="end", dag=dag)

start >> check_ran >> create_temp >> download >> spark_job >> remove_temp >> end