import logging
import json
from pyspark.sql import SQLContext, SparkSession
import datetime as dt
from pyspark import SparkFiles
from minio import Minio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

with open("/opt/spark/examples/jars/config.json", "r") as f:
    config = json.load(f)

FILEURL = config["FILEURL"]
# DRIVER_PATH = os.environ["driver_path"]

#PG_IP = Variable.get("pg_ip")

#DRIVER_PATH = Variable.get("driver_path")
s3accessKeyAws = "admin"
s3secretKeyAws = "adminpassword"
connectionTimeOut = "600000"
endpoint = "mystack-minio:9000"  #"34.27.128.193:30002",
spark = SparkSession.builder.appName("owidDataAnalyzing").getOrCreate()


def get_data():
    logging.info(f"executed at  {dt.datetime.now()}")
    logging.info(f"Reading {FILEURL}")
    sourceBucket = "airquino/raw"
    inputPath = f"s3a://$sourceBucket/2023-12-15T11:00:00+00:00.json"
    df = spark.read.json(inputPath, header=True, inferSchema= True)
    logging.info(f"Reading ok")
    return df 

def save_in_minio(df):

    logging.info(f"Writting loading")

    client = Minio(
        endpoint,
        access_key="admin",
        secret_key="adminpassword",
        secure=False
    )
    if not client.bucket_exists("airquino"):
      client.make_bucket("airquino")
    outputPath = f"s3a://airquino/raw/{dt.date.today()}.csv"
    df.write.mode("overwrite").csv(outputPath)
    logging.info(f"Writting ok")

    return True




def main():
    df = get_data()
    save_in_minio(df)
    return True

if __name__ == "__main__":
    main()
