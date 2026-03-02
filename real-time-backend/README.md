# Real-time Backend

A modular real-time data backend with an API, stream processors (Spark/Flink), Kafka, and monitoring (Prometheus + Grafana).

## Services
- API (FastAPI)
- Kafka (Bitnami, KRaft mode)
- Spark streaming app (placeholder)
- Flink job (placeholder)
- Prometheus + Grafana

## Prerequisites
- Docker and Docker Compose

## Quick start
- Start stack: `docker compose up -d`
- API health: http://localhost:8000/health
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default admin/admin)

## Environment
Edit `.env` to set:
- `API_PORT` (default 8000)
- `KAFKA_BROKERS` (default `kafka:9092`)
- `KAFKA_TOPIC` (default `climate.readings`)

## Development
- Send test events: `python scripts/load_sample_data.py`
- Implement stream logic in `spark-app/stream_processor.py` or `flink-app/flink_job.py`.

## Security/TLS
See `docker-compose.secure.override.yml` and `certificates/` to enable SSL for Kafka and clients.
