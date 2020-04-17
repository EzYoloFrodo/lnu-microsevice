import pika
import time
import os


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


print("connection success")
channel = connection.channel()

channel.queue_declare(queue='ted')


def send_message(message):
    channel.basic_publish(exchange='',
                          routing_key='ted',
                          body=message)
    print("message send! ")


def close_connection():
    connection.close()
