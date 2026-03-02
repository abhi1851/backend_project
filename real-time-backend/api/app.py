import os
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from db import CassandraClient

REQUESTS = Counter('api_requests_total', 'Total API requests')
app = Flask(__name__)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "rt_backend")

db = CassandraClient(CASSANDRA_HOST, KEYSPACE)

@app.route("/api/data/daily-avg")
def daily_avg():
    REQUESTS.inc()
    rows = db.query("SELECT * FROM metric_daily_avg LIMIT 120;")
    return jsonify([dict(r._asdict()) for r in rows])

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
