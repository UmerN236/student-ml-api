# student-ml-api

[![Pull Request CI](https://github.com/UmerN236/student-ml-api/actions/workflows/ci.yml/badge.svg)](https://github.com/UmerN236/student-ml-api/actions/workflows/ci.yml)
[![Release Container Image](https://github.com/UmerN236/student-ml-api/actions/workflows/release.yml/badge.svg)](https://github.com/UmerN236/student-ml-api/actions/workflows/release.yml)

A small FastAPI prediction service demonstrating a production-style MLOps path from pull request to an immutable, traceable container image.

## API

- `GET /health` reports application and model versions.
- `POST /predict` accepts `{"value": 10}` and returns `{"input": 10, "prediction": 20}`.
- `GET /docs` provides FastAPI's interactive OpenAPI documentation.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
python app.py
```

## Docker

```bash
docker build -t student-ml-api:1.1.0 .
docker run --rm -p 5000:5000 student-ml-api:1.1.0
curl http://localhost:5000/health
```

Published releases are available from GHCR:

```bash
docker pull ghcr.io/umern236/student-ml-api:1.1.0
docker run --rm -p 5000:5000 ghcr.io/umern236/student-ml-api:1.1.0
```

Application code enters protected `main` through pull requests. PR CI tests and build-checks the image without publishing; semantic tags trigger the separate GHCR release workflow. See [the assignment report](docs/assignment-report.md) for evidence, traceability, rollback, failure analysis, and viva answers.
