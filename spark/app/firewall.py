# -*- coding: utf-8 -*-

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
csv_file = "/usr/local/spark/resources/data/firewall.csv"
postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

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
print("Number of rows before sampling: {}".format(df_csv.count())) 
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
    .option("dbtable", "public.firewall")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)