# Kafka

The stack uses Bitnami Kafka in KRaft mode (no ZooKeeper). Useful commands:

- Create topic (from host):
  docker compose exec kafka kafka-topics.sh --create --topic climate.readings --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

- List topics:
  docker compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092

- Describe topic:
  docker compose exec kafka kafka-topics.sh --describe --topic climate.readings --bootstrap-server kafka:9092
