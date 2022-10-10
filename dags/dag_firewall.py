from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"

csv_file = "/usr/local/spark/resources/data/firewall.csv"

postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

postgres_driver_jar = "/usr/local/spark/resources/jars/postgresql-9.4.1207.jar"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="spark-firewall-module", 
    description="This DAG runs a pyspark app and it's a sample of integration between Spark and DB.",
    default_args=default_args, 
    schedule_interval=timedelta(1)
)

start = DummyOperator(task_id="start", dag=dag)

spark_job = SparkSubmitOperator(
    task_id="firewall_spark_job",
    application="/usr/local/spark/app/firewall_dag.py", 
    name="firewall-module",
    conn_id="spark_default",
    verbose=1,
    conf={
        "spark.master":spark_master,
    },
    application_args=[csv_file, postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag
)

end = DummyOperator(task_id="end", dag=dag)

start >> spark_job >> end