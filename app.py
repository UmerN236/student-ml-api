import math
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, field_validator


APPLICATION_NAME = "student-ml-api"
VERSION_FILE = Path(__file__).with_name("VERSION")


def get_version() -> str:
    """Return the application version bundled with this release."""
    return VERSION_FILE.read_text(encoding="utf-8").strip()


class PredictionRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    value: int | float

    @field_validator("value")
    @classmethod
    def value_must_be_finite(cls, value: int | float) -> int | float:
        if not math.isfinite(value):
            raise ValueError("value must be finite")
        return value


def create_app() -> FastAPI:
    app = FastAPI(title=APPLICATION_NAME, version=get_version())

    @app.get("/health", tags=["service"])
    def health():
        return {
            "status": "healthy",
            "application": APPLICATION_NAME,
            "version": get_version(),
        }

    @app.post("/predict", tags=["prediction"])
    def predict(payload: PredictionRequest):
        return {"input": payload.value, "prediction": payload.value * 2}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=5000)
