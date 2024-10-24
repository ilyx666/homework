import redis
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str


@app.post("/convert")
async def convert_currency(request: ConvertRequest):
    try:
        from_rate = redis_client.get(request.from_currency)
        to_rate = redis_client.get(request.to_currency)

        if not from_rate or not to_rate:
            raise ValueError("currency rate not found")

        converted_amount = request.amount * (float(to_rate) / float(from_rate))

        logger.info(f"converted {request.amount} {request.from_currency} to {converted_amount} {request.to_currency}")
        return {"converted_amount": converted_amount}

    except Exception as e:
        logger.error(f"failed: {e}")
        return {"error": str(e)}
