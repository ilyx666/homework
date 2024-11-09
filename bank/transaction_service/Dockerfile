FROM python:3.10-alpine

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ../transaction_service /app/transaction_service
COPY ../config.py /app/config.py
COPY ../utils /app/utils

CMD ["python", "transaction_service/app.py"]
