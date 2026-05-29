# Real-time Backend

A modular real-time data backend with an API, stream processors (Spark/Flink), Kafka, and monitoring (Prometheus + Grafana).

## Services
- API (Flask)
- Kafka (Bitnami, KRaft mode)
- Flink job (`input-events` -> `processed-events`)
- Spark streaming app (`processed-events` -> Cassandra daily aggregates)
- Prometheus + Grafana

## Prerequisites
- Docker and Docker Compose

## Quick start
- Start stack: `docker compose up -d`
- API health: http://localhost:8000/health
- Daily averages: http://localhost:8000/api/data/daily-avg
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default admin/admin)

## Environment
Edit `.env` to set:
- `API_PORT` (default 8000)
- `KAFKA_BROKER` (default `kafka:9092`)
- `KAFKA_TOPIC` (default `climate.readings`)

## Development
- Send test events: `python scripts/load_sample_data.py`
- Ingest the Delhi climate CSV: `python scripts/ingest_delhi_climate.py data/DailyDelhiClimateTrain.csv`
- Stream logic lives in `spark-app/stream_processor.py` and `flink-app/flink_job.py`.

## Security/TLS
See `docker-compose.secure.override.yml` and `certificates/` to enable SSL for Kafka and clients.
