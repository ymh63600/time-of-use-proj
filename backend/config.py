from dataclasses import dataclass

from fastapi.responses import PlainTextResponse


class Config:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    DB_URL = 'postgresql://admin:admin@localhost:5432/admin'
    MAIL_KEY = 'ilfc fqzt jgmp ktkz'

@dataclass
class DefaultResponse:
    doc: dict
    response: PlainTextResponse


class Response:
    OK = DefaultResponse(
        {"description": "OK", "content": {"text/plain": {"example": "OK"}}},
        PlainTextResponse("OK", 200),
    )

    BAD_REQUEST = DefaultResponse(
        {
            "description": "Bad Request",
            "content": {"text/plain": {"example": "Bad Request"}},
        },
        PlainTextResponse("Bad Request", 400),
    )

    UNAUTHORIZED = DefaultResponse(
        {
            "description": "Unauthorized",
            "content": {"text/plain": {"example": "Unauthorized"}},
        },
        PlainTextResponse("Unauthorized", 401),
    )

    NOT_FOUND = DefaultResponse(
        {
            "description": "Not Found",
            "content": {"text/plain": {"example": "Not Found"}},
        },
        PlainTextResponse("Not Found", 404),
    )

    INTERNAL_SERVER_ERROR = DefaultResponse(
        {
            "description": "Internal Server Error",
            "content": {"text/plain": {"example": "Internal Server Error"}},
        },
        PlainTextResponse("Internal Server Error", 500),
    )
