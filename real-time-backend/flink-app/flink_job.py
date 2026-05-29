import os, json, datetime
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.typeinfo import Types

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    source = (KafkaSource.builder()
              .set_bootstrap_servers(KAFKA_BROKER)
              .set_topics("input-events")
              .set_group_id("flink-consumer")
              .set_value_only_deserializer(SimpleStringSchema())
              .build())

    sink = (KafkaSink.builder()
            .set_bootstrap_servers(KAFKA_BROKER)
            .set_record_serializer(
                KafkaRecordSerializationSchema.builder()
                .set_topic("processed-events")
                .set_value_serialization_schema(SimpleStringSchema())
                .build())
            .build())

    ds = env.from_source(
        source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name="input",
    )

    def transform(s: str) -> str:
        try:
            o = json.loads(s)
            key = str(o.get("key", "unknown"))
            val = float(o.get("value", 0.0))
            ts = o.get("ts") or datetime.datetime.now(datetime.UTC).isoformat()
            return json.dumps({"key": key, "value": val, "ts": ts})
        except Exception:
            return json.dumps({"key": "bad", "value": 0.0, "ts": datetime.datetime.now(datetime.UTC).isoformat()})

    ds.map(transform, output_type=Types.STRING()).sink_to(sink)
    env.execute("pyflink-job")

if __name__ == "__main__":
    main()
