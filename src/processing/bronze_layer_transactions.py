from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, BooleanType
from config import create_spark_session

KAFKA_SERVER = "localhost:9092"
TRANSACTIONS_TOPIC = "finstream.transactions"

if __name__ == "__main__":
    print("Starting FinStream Bronze Layer for Transactions...")