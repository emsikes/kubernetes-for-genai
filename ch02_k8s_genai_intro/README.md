# Ch02 — Kubernetes: Introduction and Integration with GenAI

## Pattern
Package a GenAI model as a production-style container with a FastAPI
inference server. Validate resource behavior before touching K8s.

## Mini-Project
**GenAI Inference Container** — a multi-stage Docker image wrapping
distilgpt2 behind a FastAPI REST API with health check and inference
endpoints.

## Implementation
| File | Purpose |
|---|---|
| `inference_app.py` | FastAPI server — model loading, inference, health check |
| `requirements-inference.txt` | Lean container-only dependencies |
| `Dockerfile` | Multi-stage build — builder stage installs deps, runtime stage runs app |

## Key Concepts
- Multi-stage Dockerfile keeps the production image lean by separating
  dependency installation from the runtime environment
- `MODEL_NAME` env var makes the image model-agnostic — swap models at
  runtime via K8s env vars without rebuilding
- Lazy model loading via module-level cache means the container passes
  health checks before the model is ready
- `host="0.0.0.0"` is required for the server to be reachable outside
  the container — localhost would be invisible to Docker port mapping
- Resource limits are enforced via Linux cgroups — same mechanism
  whether set via `docker run` flags or K8s resource manifests

## Resource Profiling Results
| Memory Limit | Result |
|---|---|
| 512MB | Container crashed on model load (exit code 2) |
| 1GB | Healthy — model loaded and inference succeeded |

**Takeaway:** Pod manifest for this container must set memory limit to
at least `1Gi`. This number was measured, not guessed.

## How to Run
```bash
cd ch02_k8s_genai_intro

# Build
docker build -t genai-inference:ch02 .

# Run with profiled resource limits
docker run --rm -p 8080:8080 --memory=1g --cpus=1 genai-inference:ch02

# Health check
curl http://localhost:8080/health

# Inference
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Kubernetes is a container orchestration platform that", "max_tokens": 50}'
