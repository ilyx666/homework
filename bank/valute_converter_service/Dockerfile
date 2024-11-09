FROM python:3.10-alpine

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ../valute_converter_service /app/valute_converter_service
COPY ../config.py /app/config.py
COPY ../utils /app/utils

CMD ["python", "valute_converter_service/app.py"]
