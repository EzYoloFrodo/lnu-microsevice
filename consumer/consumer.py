#!/usr/bin/env python
import pika
import os
import time
import sys
from pymongo import MongoClient
import json


rmq_url_connection_str = os.environ.get("AMQP_URL")

client = MongoClient('mongodb://root:example@localhost:27017')
db = client["news"]

while True:
    try:
        parameters = pika.URLParameters(rmq_url_connection_str)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        break
    except Exception:
        print("retry")
        time.sleep(10)

channel.queue_declare(queue='ted')


def on_message(channel, method_frame, header_frame, body):
    body_str = body.decode("utf-8")
    json_data = json.loads(body_str)
    print(type(json_data))
    print(json_data)
    db.posts.insert_one(json_data).inserted_id


channel.basic_consume(on_message, queue='ted')
try:
    channel.start_consuming()
except Exception as e:
    print(e)
    channel.stop_consuming()
    print("stop_consuming")
