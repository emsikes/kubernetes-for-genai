# Stage 1: Builder
# A full Python image used only to install dependencies
# Keeping installation separate in a stage means the final
# image doen't carry pip, build tools, or cache layers into prod
FROM python:3.11-slim AS builder
WORKDIR /build

COPY requirements-inference.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-inference.txt

# Stage 2: Runtime
# A clean slim image - only installed packages are copied in from
# the builder stage, not the build tooling that produced them.
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder stage only
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY inference_app.py .

# MODEL_NAME can be overwritten at runtime via docker run -e or K8s env vars
ENV MODEL_NAME=distilgpt2

# Expose the port uvicorn will listen on
EXPOSE 8000

# Invoke uvicorn directly - not via the __main__ block in inference_app.py.
# This is the production endpoint inside the container
CMD ["uvicorn", "inference_app:app", "--host", "0.0.0.0", "--port", "8080"]
