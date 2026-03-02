import os, json, time, random, datetime, subprocess

BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
topic = "input-events"

def send(msg: str):
    cmd = f"docker compose exec -T kafka bash -lc \"echo '{msg}' | kafka-console-producer.sh --broker-list kafka:9092 --topic {topic} > /dev/null\""
    subprocess.check_call(cmd, shell=True)

keys = ["alpha", "beta", "gamma"]
print("Sending 100 sample events to Kafka ...")
for i in range(100):
    o = {"key": random.choice(keys),
         "value": round(random.random()*100, 2),
         "ts": datetime.datetime.now(datetime.UTC).isoformat()}
    send(json.dumps(o))
    time.sleep(0.1)
print("Done.")
