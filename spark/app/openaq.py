# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

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
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") 
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider") 
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .getOrCreate()
)
sc = spark.sparkContext
sc.setLogLevel("WARN")

####################################
# Parameters
####################################
s3path =  "s3a://openaq-fetches/daily/2017-08-11.csv"

####################################
# Read CSV Data
####################################
print("######################################")
print("READING S3 FILE")
print("######################################")

df_s3 = (
    spark.read
    .format("csv")
    .option("header", False)
    .load(s3path)
)

# df = spark.read.csv(s3path, header=False)

print("######################################")
print("SAMPLING CSV DATA")

df_s3_sample = df_s3.sample(0.1, 3)

print("Number of rows after sampling: {}".format(df_s3_sample.count())) 
print("######################################")

print("######################################")
print("PRINTING 10 ROWS OF SAMPLE DF")
print("######################################")

df_s3_sample.show(10)

