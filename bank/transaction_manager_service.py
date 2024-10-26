import pika
import json
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from config import TRANSACTION_QUEUE
from utils.converter_client import CurrencyConverterClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class TransactionRequest(BaseModel):
    sender_id: int
    initial_amount: float
    currency: str
    receiver_id: int


@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit_transaction/")
def process_transaction(
        sender_id: int = Form(...),
        initial_amount: float = Form(...),
        currency: str = Form(...),
        receiver_id: int = Form(...)
):
    converter = CurrencyConverterClient()
    converted_amount = converter.convert_currency(currency, initial_amount)

    transaction_data = {
        "sender_id": sender_id,
        "initial_amount": initial_amount,
        "currency": currency,
        "receiver_id": receiver_id,
        "amount_in_rub": converted_amount
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=TRANSACTION_QUEUE, durable=True)
    channel.basic_publish(exchange='', routing_key=TRANSACTION_QUEUE, body=json.dumps(transaction_data))
    connection.close()

    return {"status": "Transaction processed"}
