import pika
import json
from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='transaction_queue', durable=True)


class TransactionRequest(BaseModel):
    account_id: int
    amount: float
    currency: str
    transaction_type: str


@app.post("/transaction")
async def create_transaction(request: TransactionRequest):
    try:
        logger.info(f"Received transaction request: {request}")

        channel.basic_publish(
            exchange='',
            routing_key='transaction_queue',
            body=json.dumps(request.dict()),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        logger.info(f"transaction request sent to RabbitMQ: {request}")
        return {"message": "transaction request sent"}
    except Exception as e:
        logger.error(f"failed to send transaction request: {e}")
        return {"error": "failed to process transaction request"}
