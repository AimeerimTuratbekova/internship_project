import os
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "file-data")

# Retry loop
for _ in range(20):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: v.encode('utf-8')
        )
        print("✅ Kafka connected.")
        break
    except NoBrokersAvailable:
        print("❌ Kafka not ready, retrying...")
        time.sleep(3)
else:
    raise Exception("❌ Failed to connect to Kafka after retries.")

# Continua con la logica di lettura file
DATA_DIR = "/data"

while True:
    for file_name in os.listdir(DATA_DIR):
        if not file_name.endswith(".json"):
            continue
        path = os.path.join(DATA_DIR, file_name)
        with open(path, "r") as f:
            data = f.read().strip()
            producer.send(KAFKA_TOPIC, data)
            # for line in f:
                # producer.send(KAFKA_TOPIC, line.strip())
        os.rename(path, path + ".sent")
        print(f"✅ Sent {file_name}")
    time.sleep(5)
