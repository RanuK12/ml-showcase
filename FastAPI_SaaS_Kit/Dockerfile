# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

# Runtime stage
FROM python:3.12-slim
RUN useradd -r -s /bin/false appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
