import csv
import datetime as dt
import json
import os
import sys

from kafka import KafkaProducer

BROKER = os.getenv("KAFKA_BROKER", "localhost:9094")
TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "input-events")

def iso_ts(date_str: str) -> str:
    # Expecting YYYY-MM-DD from DailyDelhiClimateTrain.csv
    d = dt.datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return d.replace(tzinfo=dt.timezone.utc).isoformat()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_delhi_climate.py data/DailyDelhiClimateTrain.csv")
        sys.exit(1)
    csv_path = sys.argv[1]
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            metrics = ["meantemp", "humidity", "wind_speed", "meanpressure"]
            sent = 0
            for r in reader:
                ts = iso_ts(r["date"])
                for m in metrics:
                    val = r.get(m)
                    if not val:
                        continue
                    try:
                        v = float(val)
                    except ValueError:
                        continue
                    producer.send(TOPIC, {"key": m, "value": v, "ts": ts})
                    sent += 1
        producer.flush()
    finally:
        producer.close()
    print(f"Sent {sent} events to topic {TOPIC}.")

if __name__ == "__main__":
    main()
