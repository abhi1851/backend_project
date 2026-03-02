FROM python:3.8
WORKDIR /app

RUN pip install apache-flink==2.0.0
# Needed for pemja (apache-flink dependency) to build native code
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jdk-headless \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

RUN pip install pemja
RUN pip install --no-cache-dir 

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY flink_job.py /app/flink_job.py
