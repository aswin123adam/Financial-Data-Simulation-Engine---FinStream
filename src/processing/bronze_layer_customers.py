from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col, current_timestamp, lit
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, BooleanType
from config import create_spark_session

KAFKA_SERVER = "localhost:9092"
CUSTOMERS_TOPIC = "finstream.customers"

CUSTOMER_SCHEMA = StructType([
    StructField("customer_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("date_of_birth", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True),
    StructField("annual_income", DoubleType(), True),
    StructField("credit_score", IntegerType(), True),
    StructField("credit_tier", StringType(), True),
    StructField("customer_segment", StringType(), True),
    StructField("customer_since", StringType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("created_at", StringType(), True),
])

def process_bronze_layer(spark, topic: str) -> DataFrame:
    df = spark.read\
        .format("kafka")\
        .option("kafka.bootstrap.servers", KAFKA_SERVER)\
        .option("subscribe", topic)\
        .option("startingOffsets", "earliest")\
        .load()
    return df

def parse_bronze_data(df: DataFrame) -> DataFrame:
    schema = "customer_id STRING, name STRING, email STRING, created_at TIMESTAMP"
    parsed_df = df\
        .selectExpr("CAST(value AS STRING) as json_data", "timestamp as kafka_timestamp")\
        .select(from_json(col("json_data"), CUSTOMER_SCHEMA).alias("data"),
                col("kafka_timestamp"))\
        .select("data.*", "kafka_timestamp")\
        .withColumn("proceessed_at", current_timestamp())
    
    return parsed_df

def save_to_parquet(df: DataFrame, path: str):
    df.write.mode("append").parquet(path)

if __name__ == "__main__":
    spark = create_spark_session("FinStream Bronze Layer Test")

    print("Reading from KAFKA topic...")

    raw_data = process_bronze_layer(spark, CUSTOMERS_TOPIC)
    processed_data = parse_bronze_data(raw_data)
    save_to_parquet(processed_data, "parquet_output/customers")
    
    print("Schema :")
    processed_data.summary().show()

    print("Processed Data from KAFKA :")
    processed_data.show(5, truncate=False)
    spark.stop()