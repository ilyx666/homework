import pika
import json
from utils.db import save_transaction_to_db


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='transaction_queue', durable=True)


def callback(ch, method, properties, body):
    transaction_data = json.loads(body)
    save_transaction_to_db(transaction_data)


channel.basic_consume(queue='transaction_queue', on_message_callback=callback, auto_ack=True)
print('ожидание сообщений...')
channel.start_consuming()
