# SPARK - AIRFLOW

## HOW TO START JUPYTER-SPARK (EDA)

From command line:

- Enter in the project dir
- Run the command ```docker build ./docker/jupyter-spark/ -f ./docker/jupyter-spark/Dockerfile.JupyterSpark -t jupyter-spark-img```
- Run the command ```docker-compose -f docker/jupyter-spark/docker-compose.JupyterSpark.yaml up```
- Open jupyter notebook

At the path 'notebooks/read-datset.ipynb' there is a script that explains how to read the dataset with spark

## HOW TO START SPARK AND AIRFLOW CONTAINERS (PIPELINE)

From command line:

- Enter in the project dir
- Run the command ```docker build . -f ./docker/spark/Dockerfile.Spark -t spark-air```
- Run the command ```docker build . -f ./docker/spark/Dockerfile.Airflow -t docker-airflow-spark```
- Run the command ```docker-compose -f docker/docker-compose.yaml up -d```
- When all the services started successfully, go to:

> - http://localhost:8282/ to check that Airflow has started successfully;
> - http://localhost:8181/ to check that Spark is up and running;
> - http://localhost:5050/ to check that Postgres Admin is running.

## POSTGRES ADMIN UI

- Log-in with email ```admin@admin.com``` and password ```airflow```
- Servers: right click --> Create --> Server
- General tab: Enter a name (ex. ```my_db```)
- Connection tab: Enter ```docker_postgres_1``` as host, ```5432``` as port and ```airflow``` as db, username and password
- Save

### QUERYING DATA

- Go to my_db --> databases --> test --> schemas --> public --> tables
- Right click on table_name --> query tool

## TEST SPARK JOB

```docker exec -it docker_spark_1 spark-submit --master spark://spark:7077 /usr/local/spark/app/<job_file>```

### CONFIGURE SPARK CONNECTION FROM AIRFLOW UI

- From Airflow UI select Admin --> Connections
- Search for spark_default and select "edit"
- Enter ```spark://spark``` as host and ```7077``` as port
- Return to the homepage: turn the DAG on, then trigger it

## USEFUL COMMANDS

Open container command line:    ```docker exec --user root -it <container_name> /bin/bash``` (esc crtl+z)
Stop all containers:            ```docker stop $(docker ps -a –q)```
Delete all containers:          ```docker rm $(docker ps -a -q)```
Delete all volumes:             ```docker volume rm $(docker volume ls -q)```

## RESOURCES

Internet firewall dataset](https://archive.ics.uci.edu/ml/datasets/Internet+Firewall+Data)
[]()
