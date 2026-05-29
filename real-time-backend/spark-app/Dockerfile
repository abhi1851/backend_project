FROM bitnamilegacy/spark:3.5.1
USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
USER 1001
WORKDIR /app
COPY stream_processor.py /app/stream_processor.py
