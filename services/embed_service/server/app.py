import logging
import logging.config
from datetime import datetime

from flask import Flask
from flask_pydantic import validate
from transformers import AutoModel, AutoTokenizer

from services.embed_service.log_config import LOG_CONFIG
from services.embed_service.server.model import (
    EmbedRequest,
    EmbedResponse,
    HealthResponse,
)

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_CONFIG)


def make_service():
    service = Flask("Text embedding service")
    with service.app_context():
        service.tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
        service.embed_model = AutoModel.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
    return service


app: Flask = make_service()


@app.route("/embed", methods=["POST"])
@validate()
def embed(body: EmbedRequest) -> EmbedResponse:
    start_time = datetime.now()
    tokenized_text = app.tokenizer(body.input_text, truncation=True, max_length=256, return_tensors="pt")
    outputs = app.embed_model(**tokenized_text)[0]
    end_time = datetime.now() - start_time
    logger.info(
        "Embed request with %d tokens took %.3f seconds",
        len(tokenized_text["input_ids"][0]),
        end_time.microseconds / 10e6,
    )
    return EmbedResponse(embeddings=outputs.squeeze().mean(dim=0).tolist())


@app.route("/health")
@validate()
def health() -> HealthResponse:
    return HealthResponse(msg="OK")
