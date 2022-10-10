# -*- coding: utf-8 -*-

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

##########################
# You can configure master here if you do not pass the spark.master paramenter in conf
##########################
#master = "spark://spark:7077"
#conf = SparkConf().setAppName("Spark App").setMaster(master)
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
csv_file = sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILE")
print("######################################")

df_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(csv_file)
)

print("######################################")
print("SAMPLING CSV DATA")

df_csv_sample = df_csv.sample(0.1, 3)

print("Number of rows after sampling: {}".format(df_csv_sample.count())) 
print("######################################")

print("######################################")
print("ADDING NEW COLUMNS")
print("######################################")

df_csv_sample = df_csv_sample.withColumn("AVG Bytes Sent", col("Bytes Sent") / col("pkts_sent"))
df_csv_sample = df_csv_sample.withColumn("AVG Bytes Received", col("Bytes Received") / col("pkts_received"))

print("######################################")
print("PRINTING 10 ROWS OF SAMPLE DF")
print("######################################")

df_csv_sample.show(10)

print("######################################")
print("LOADING POSTGRES TABLE")
print("######################################")


(
    df_csv_sample.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.firewall_dag")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)
