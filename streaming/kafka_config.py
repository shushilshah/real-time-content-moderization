# from kafka import KafkaProducer
# import json


# def get_producer():
#     try:
#         producer = KafkaProducer(
#             bootstrap_servers="localhost:9092",
#             value_serializer=lambda v: json.dumps(v).encode("utf-8")
#         )
#         return producer
#     except Exception as e:
#         print("⚠️ Kafka not available:", e)
#         return None

import os
from kafka import KafkaProducer

def get_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )