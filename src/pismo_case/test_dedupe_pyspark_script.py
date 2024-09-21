import pytest
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window


@pytest.fixture(scope="session")
def spark():
    # Initialize a Spark session for testing
    return SparkSession.builder.master("local").appName("PySparkTest") \
        .getOrCreate()


def deduplicate_events(df):
    """
    Function to deduplicate events, keeping the latest event for each
    event_id based on timestamp.
    """
    window_spec = Window.partitionBy("event_id").orderBy(
        col("timestamp").desc()
    )
    dedup_df = (
        df.withColumn("row_num", row_number().over(window_spec))
        .filter(col("row_num") == 1)
        .drop("row_num")
    )
    return dedup_df


def test_deduplication(spark):
    """
    Pytest to verify that only the latest event (based on timestamp)
    is kept for each event_id.
    """

    # Create a mock dataset with duplicates
    data = [
        Row(event_id="1", timestamp="2023-09-20T10:00:00",
            event_type="created"),
        Row(
            event_id="1", timestamp="2023-09-21T12:00:00",
            event_type="updated"),  # Latest
        Row(
            event_id="2", timestamp="2023-09-19T08:00:00",
            event_type="created"),  # No duplicates
        Row(event_id="3", timestamp="2023-09-18T07:00:00",
            event_type="status-change"),
        Row(
            event_id="3", timestamp="2023-09-18T09:00:00",
            event_type="status-change"),  # Latest
        Row(event_id="3", timestamp="2023-09-18T08:30:00",
            event_type="status-change"),
    ]

    # Create DataFrame from the mock data
    df = spark.createDataFrame(data)

    # Apply deduplication
    dedup_df = deduplicate_events(df)

    # Collect the results into a list of rows
    result = dedup_df.orderBy("event_id").collect()

    # Define the expected result: Only the latest event for each event_id
    expected_data = [
        Row(
            event_id="1", timestamp="2023-09-21T12:00:00",
            event_type="updated"),  # Latest for event_id=1
        Row(
            event_id="2", timestamp="2023-09-19T08:00:00",
            event_type="created"),  # Only one for event_id=2
        Row(
            event_id="3", timestamp="2023-09-18T09:00:00",
            event_type="status-change"),  # Latest for event_id=3
    ]

    # Verify the length of the result matches the expected length
    assert len(result) == len(expected_data)

    # Verify that each row in the result matches the expected row
    for row, expected in zip(result, expected_data):
        assert row["event_id"] == expected["event_id"]
        assert row["timestamp"] == expected["timestamp"]
        assert row["event_type"] == expected["event_type"]
