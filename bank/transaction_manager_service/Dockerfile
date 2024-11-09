FROM python:3.10-alpine

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ../transaction_manager_service /app/transaction_manager_service
COPY ../config.py /app/config.py
COPY ../templates /app/templates
COPY ../utils /app/utils

CMD ["uvicorn", "transaction_manager_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
