import os
from pyspark.sql import SparkSession, functions as F, types as T
from cassandra.cluster import Cluster

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "rt_backend")

spark = SparkSession.builder.appName("spark-structured-streaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

raw = (spark.readStream.format("kafka")
       .option("kafka.bootstrap.servers", KAFKA_BROKER)
       .option("subscribe", "processed-events")
       .option("startingOffsets", "latest")
       .load())

df = raw.select(F.col("value").cast("string").alias("value"))

schema = T.StructType([
    T.StructField("key", T.StringType()),
    T.StructField("value", T.DoubleType()),
    T.StructField("ts", T.TimestampType()),
])

json_df = df.select(F.from_json("value", schema).alias("j")).select("j.*")

# Daily bucket + per-metric aggregation
daily = json_df.withColumn("bucket_date", F.to_date("ts"))
agg = (daily
       .groupBy(F.col("bucket_date"), F.col("key"))
       .agg(F.count("*").alias("count"),
            F.avg("value").alias("avg_value"))
       .select(F.col("bucket_date").alias("bucket_ts"),
               F.col("key"), F.col("count"), F.col("avg_value")))

def write_to_cassandra(batch_df, batch_id):
    rows = batch_df.collect()
    if not rows:
        return
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect()
    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} "
        "WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' };"
    )
    session.set_keyspace(KEYSPACE)
    session.execute("""
        CREATE TABLE IF NOT EXISTS metric_daily_avg (
            bucket_ts date,
            key text,
            count bigint,
            avg_value double,
            PRIMARY KEY (bucket_ts, key)
        ) WITH CLUSTERING ORDER BY (key ASC);
    """)
    prepared = session.prepare(
        "INSERT INTO metric_daily_avg (bucket_ts, key, count, avg_value) VALUES (?, ?, ?, ?)"
    )
    for r in rows:
        session.execute(prepared, (
            r['bucket_ts'], r['key'], int(r['count']),
            float(r['avg_value']) if r['avg_value'] is not None else None
        ))
    session.shutdown()
    cluster.shutdown()

query = (agg.writeStream
         .foreachBatch(write_to_cassandra)
         .outputMode("update")
         .trigger(processingTime="10 seconds")
         .start())

query.awaitTermination()