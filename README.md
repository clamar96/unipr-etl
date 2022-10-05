# HOW TO START JUPYTER-SPARK (EDA)

From command line:

- Enter in the project dir
- Run the command ```docker build .\docker\jupyter-spark\ -f .\docker\jupyter-spark\Dockerfile.JupyterSpark -t jupyter-spark-img```
- Run the command ```docker-compose -f docker/jupyter-spark/docker-compose.JupyterSpark.yml up```
- Open jupyter notebook

At the path 'notebooks/read-datset.ipynb' there is a script that explains how to read the dataset with spark
