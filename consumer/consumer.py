#!/usr/bin/env python
import pika
import os
import time
import sys


rmq_url_connection_str = os.environ.get("AMQP_URL")

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
    print(body_str)


channel.basic_consume(on_message, queue='ted')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    rmq_tools.console_log("Ошибка:\n", traceback.format_exc())
