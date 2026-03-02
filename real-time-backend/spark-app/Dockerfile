FROM bitnamilegacy/spark:3.5.1
USER root
RUN pip install --no-cache-dir pyspark==3.5.1 cassandra-driver==3.29.2
USER 1001
WORKDIR /app
COPY stream_processor.py /app/stream_processor.py