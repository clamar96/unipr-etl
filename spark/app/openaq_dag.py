# -*- coding: utf-8 -*-

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

##########################
# You can configure master here if you do not pass the spark.master paramenter in conf
##########################
#master = "spark://spark:7077"
#conf = SparkConf().setAppName("Spark Firewall App").setMaster(master)
#sc = SparkContext(conf=conf)
#spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Create spark session
spark = (
    SparkSession
    .builder
    .getOrCreate()
)
sc = spark.sparkContext
sc.setLogLevel("WARN")

####################################
# Parameters
####################################
path =  sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]

print("######################################")
print("READING FILE")
print("######################################")

df = (
    spark.read
    .format("csv")
    .option("header", False)
    .load(path)
)

print("######################################")
print("FILTERING ROWS")

df = df.filter(col("_c4")=="IT")

print("######################################")

print("######################################")
print("LOADING POSTGRES TABLE")
print("######################################")

(
    df.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.openaq")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("append")
    .save()
)
