import pika
import json
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='transaction_queue', durable=True)


def callback(ch, method, properties, body):
    message = json.loads(body)
    logger.info(f"received transaction message: {message}")
    logger.info(f"processed transaction for account_id: {message['account_id']}")


channel.basic_consume(queue='transaction_queue', on_message_callback=callback, auto_ack=True)

logger.info('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
