#!/usr/bin/env python
import pika
import os
import time
import sys
from pymongo import MongoClient
import json

client = MongoClient("mongo", 27017, username="root", password="example")
db = client["news"]

rmq_url_connection_str = os.environ.get("AMQP_URL")


def save_in_db(json_data):
    print('start inserting')
    new_data = {
        "link": json_data.get("link"),
        "title": json_data.get("title"),
        "text": str(json_data.get("text")),
        "author_name": json_data.get("author_name")
    }

    db.posts.insert_one(new_data)
    print("insert one done")


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
    print(json_data["text"])
    print(type(json_data["text"]))
    save_in_db(json_data)


channel.basic_consume(on_message, queue='ted')

try:
    channel.start_consuming()
except Exception as e:
    print(e)
    channel.stop_consuming()
    print("stop_consuming")
