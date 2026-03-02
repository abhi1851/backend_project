import sys, os, csv, subprocess, datetime as dt

BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "input-events")

def send(msg: str):
    cmd = f"docker compose exec -T kafka bash -lc \"echo '{msg}' | kafka-console-producer.sh --broker-list kafka:9092 --topic {TOPIC} > /dev/null\""
    subprocess.check_call(cmd, shell=True)

def iso_ts(date_str: str) -> str:
    # Expecting YYYY-MM-DD from DailyDelhiClimateTrain.csv
    d = dt.datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return d.replace(tzinfo=dt.timezone.utc).isoformat()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_delhi_climate.py data/DailyDelhiClimateTrain.csv")
        sys.exit(1)
    csv_path = sys.argv[1]
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
                msg = f'{{"key":"{m}","value":{v},"ts":"{ts}"}}'
                send(msg)
                sent += 1
    print(f"Sent {sent} events to topic {TOPIC}.")

if __name__ == "__main__":
    main()