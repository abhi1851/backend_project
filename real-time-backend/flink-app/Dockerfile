FROM python:3.8
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl openjdk-17-jdk-headless \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/java \
    && ln -s "$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")" /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

ARG FLINK_KAFKA_CONNECTOR_VERSION=3.2.0-1.19
RUN curl -fsSL \
    "https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_KAFKA_CONNECTOR_VERSION}/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar" \
    -o "/usr/local/lib/python3.8/site-packages/pyflink/lib/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar"

COPY flink_job.py /app/flink_job.py
