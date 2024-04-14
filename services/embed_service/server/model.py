from typing import List, Union

from pydantic import BaseModel, Field


class EmbedRequest(BaseModel):
    input_text: str


class EmbedResponse(BaseModel):
    embeddings: List[float]


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")


class ValidationError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str  # noqa: A003


class ValidationErrorResponse(BaseModel):
    errors: List[ValidationError]
