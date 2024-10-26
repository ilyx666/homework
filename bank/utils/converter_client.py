import json
import uuid

import pika


class CurrencyConverterClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True, durable=True).method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def convert_currency(self, currency, amount):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        request_data = json.dumps({"currency": currency, "amount": amount})

        self.channel.basic_publish(
            exchange='',
            routing_key='currency_conversion_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request_data
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response["amount_in_rub"]