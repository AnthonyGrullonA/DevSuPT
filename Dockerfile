FROM python:3.11-slim

LABEL maintainer="Jairol Anthony Grullon Amparo"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD curl --fail http://localhost:8000/api/ || exit 1

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
