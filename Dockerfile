FROM python:3.12.11-slim

ARG APP_VERSION=dev
ARG VCS_REF=unknown
ARG BUILD_DATE=unknown
ARG REPOSITORY=https://github.com/UmerN236/student-ml-api

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.description="A small, tested ML prediction API" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="${REPOSITORY}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py VERSION ./

RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "2"]
