import logging
import os
from functools import lru_cache
from typing import Any, Dict

import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Входные данные
class TextRequest(BaseModel):
    text: str


# Простейший кеш через lru_cache
@lru_cache(maxsize=128)
def cached_classification(text: str) -> Dict[str, Any]:
    logger.info(f"Запрос к внешнему API для текста: {text}")
    try:
        # Нужен токен: exportF_API H_TOKEN="полученный вами токен"
        HF_API_TOKEN = os.getenv("HF_API_TOKEN")
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        # headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
        payload = {"inputs": text}

        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-roberta-base-sentiment-latest",
            headers=headers,
            json=payload,
        )

        response.raise_for_status()
        data = response.json()

        # Приведение к единому формату
        if isinstance(data, list) and isinstance(data[0], list):
            data = data[0]

        labels = [item["label"] for item in data]
        scores = [item["score"] for item in data]

        return {"labels": labels, "scores": scores}
    except Exception as e:
        logger.error(f"Ошибка при вызове API: {e}")
        raise HTTPException(status_code=503, detail="ML сервис временно недоступен")


@app.post("/classify")
async def classify_text(req: TextRequest):
    try:
        result = cached_classification(req.text)
        # Проверка: был ли результат из кеша
        cached = cached_classification.cache_info().hits > 0
        return {
            "labels": result["labels"],
            "scores": result["scores"],
            "cached": cached,
        }
    except HTTPException as e:
        raise e


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
