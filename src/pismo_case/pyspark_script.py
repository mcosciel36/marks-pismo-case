from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder.appName("EventProcessor").getOrCreate()

# Load the data
df = spark.read.json("events.json")

# Deduplication: Keep the latest event by event_id
window_spec = Window.partitionBy("event_id").orderBy(col("timestamp").desc())
dedup_df = df.withColumn("row_num", row_number().over(window_spec)).filter(col("row_num") == 1).drop("row_num")

# Partition by year, month, day, and event type
dedup_df = dedup_df.withColumn("year", col("timestamp").substr(1, 4))\
                   .withColumn("month", col("timestamp").substr(6, 2))\
                   .withColumn("day", col("timestamp").substr(9, 2))

# Save as Parquet partitioned by year, month, day, event_type
dedup_df.write.mode("overwrite").partitionBy("year", "month", "day", "event_type").parquet("output_directory/")
