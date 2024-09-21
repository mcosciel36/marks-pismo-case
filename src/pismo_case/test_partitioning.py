from pyspark.sql import SparkSession
import os

def test_parquet_partitioning():
    spark = SparkSession.builder.appName("Test").getOrCreate()

    # Assuming that the Parquet files are written in the 'output_directory'
    df = spark.read.parquet("output_directory")

    # Ensure partition columns exist
    assert "year" in df.columns
    assert "month" in df.columns
    assert "day" in df.columns
    assert "event_type" in df.columns

    # Check if the directory structure follows the partitioning
    partitions = ["output_directory/year=2021/month=02/day=08/event_type=created"]
    for partition in partitions:
        assert os.path.exists(partition)

    spark.stop()
