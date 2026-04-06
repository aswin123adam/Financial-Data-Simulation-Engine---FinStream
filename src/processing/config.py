from pyspark.sql import SparkSession

KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0"

def create_spark_session(app_name: str) -> SparkSession:
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.jars.packages", KAFKA_PACKAGE) \
        .config("spark.sql.streaming.checkpointLocation", "checkpoint") \
        .config("spark.driver.host", "localhost") \
        .config("spark.ui.enabled", "false") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark


if __name__ == "__main__":
    spark = create_spark_session("FinStream Test")
    print("SparkSession created successfully!")
    print(f"Spark version: {spark.version}")
    spark.stop()