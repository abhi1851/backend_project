import datetime
import json
import os
import random
import time

from kafka import KafkaProducer

BROKER = os.getenv("KAFKA_BROKER", "localhost:9094")
TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "input-events")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

keys = ["alpha", "beta", "gamma"]
print("Sending 100 sample events to Kafka ...")
for i in range(100):
    o = {"key": random.choice(keys),
         "value": round(random.random()*100, 2),
         "ts": datetime.datetime.now(datetime.UTC).isoformat()}
    producer.send(TOPIC, o)
    time.sleep(0.1)
producer.flush()
producer.close()
print("Done.")
