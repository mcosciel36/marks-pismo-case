from pyspark.sql import SparkSession

# Initialize the Spark session
spark = SparkSession.builder.appName("ParquetToJson").getOrCreate()

# Path to the Parquet files
parquet_path = "output_directory"

# Read the Parquet files
df = spark.read.parquet(parquet_path)

# Show the schema to verify the structure
df.printSchema()

# Show some data for verification
df.show(truncate=False)

# Write the DataFrame to a new directory in JSON format
json_output_path = "json_output_directory/"

# Write the DataFrame to JSON files in the specified output directory
df.write.mode("overwrite").json(json_output_path)

# Stop the Spark session
spark.stop()
