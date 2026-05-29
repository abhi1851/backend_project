import os
import datetime as dt
import decimal
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from db import CassandraClient

REQUESTS = Counter('api_requests_total', 'Total API requests')
app = Flask(__name__)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "rt_backend")

db = CassandraClient(CASSANDRA_HOST, KEYSPACE)

def json_safe(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, decimal.Decimal):
        return float(value)
    return str(value)

def row_to_dict(row):
    return {key: json_safe(value) for key, value in row._asdict().items()}

@app.route("/api/data/daily-avg")
def daily_avg():
    REQUESTS.inc()
    rows = db.query("SELECT * FROM metric_daily_avg LIMIT 120;")
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/health")
def health():
    REQUESTS.inc()
    cassandra_ready = db.is_connected()
    status_code = 200 if cassandra_ready else 503
    return jsonify({
        "status": "ok" if cassandra_ready else "degraded",
        "dependencies": {
            "cassandra": "ok" if cassandra_ready else "unavailable"
        }
    }), status_code

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
