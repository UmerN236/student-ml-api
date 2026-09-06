import math
from pathlib import Path

from flask import Flask, jsonify, request


APPLICATION_NAME = "student-ml-api"
MODEL_VERSION = "model-1"
VERSION_FILE = Path(__file__).with_name("VERSION")


def get_version() -> str:
    """Return the application version bundled with this release."""
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(
            status="healthy",
            application=APPLICATION_NAME,
            application_version=get_version(),
            model_version=MODEL_VERSION,
        )

    @app.post("/predict")
    def predict():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or "value" not in payload:
            return jsonify(error="Missing required field: value"), 400

        value = payload["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return jsonify(error="Field 'value' must be a number"), 400
        if not math.isfinite(value):
            return jsonify(error="Field 'value' must be finite"), 400

        return jsonify(input=value, prediction=value * 2)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
