"""
FastAPI inference server that wraps a HuggingFace text generation model.

This will demonstrate the core container patter for GenAI model serving: 
A lightweight HTTP server that loads a model once and exposes it via
a REST endpoint, and will get packaged into a Docker image.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel

from transformers import pipeline, Pipeline


# Read MODEL_NAME from the environment so the container can serve different
# models at runtime wwithout a rebuild - can just change the env var in the K8s manifest
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")

# Module level cache - load the model once for optimal performance
_model: Pipeline | None = None

def load_model() -> Pipeline:
    """
    Lazy loading the HuggingFace pipeline on the first call and cache it globally.

    Conntainer will pass health checks before the model is ready since liveness
    and readiness probes will run succesfully upon container startup.
    """
    global _model
    if _model is None:
        print(f"Loading mode: {MODEL_NAME}")
        _model = pipeline("text-generation", model=MODEL_NAME)
        print("Model loaded successfully")
    return _model


def generate_text(prompt: str, max_tokens: int = 100) -> str:
    """
    Run inference against the loaded model and return the generated text.

    max_new_tokens controls output length independantly of the input prompt length
    - import for predicatable container memory under load. 

    truncation_true=True ensures long prompts don't cause out of memory errors
    inside the container
    """
    model = load_model()

    output = model(
        prompt,
        max_new_tokens=max_tokens,
        truncation=True,
        pad_token_id=model.tokenizer.eos_token_id,
    )

    # The pipeline returns a list of dicts and here we extract the generated string
    return output[0]["generated_text"]

# FastAPI routes defined here and in Kubernetes this will be the process
# that uvicorn will serve from inside the container
app = FastAPI(title="GenAI Inference Server")

class GenerateRequest(BaseModel):
    """Request nody schema for the /generate endpoint"""
    prompt: str
    max_tokens: int = 100


class GenerateResponse(BaseModel):
    """Response body for schema for the /generate endpoint"""
    generated_text: str
    model_name: str


@app.get("/health")
def health_check() -> dict:
    """
    Liveness probe endpoint for Kubernetes.

    K8s will call this route to determine if the container is running.
    Returning 200 OK is sufficient for this check.  If the process is
    dead, the endpoint won't respond and K8s will restart the container.
    """
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    """
    Inference endpoint that accepts a prompt and returns generated text.

    FastAPI validates the request body against GenerateRequest and the 
    response against GenerateResponse via Pydantic.  This is the endpoint 
    the K8s Services will router external traffic to.
    """
    generated_text = generate_text(request.prompt, request.max_tokens)

    return GenerateResponse(
        generated_text=generated_text,
        model_name=MODEL_NAME,
    )

if __name__ == "__main__":
    import uvicorn
    # Entry point for local development, in the container, uvicorn
    # is invoked directly via the Dockerfile CMD instruction instead
    uvicorn.run("inference_app:app", host="0.0.0.0", port=8000, reload=False)
