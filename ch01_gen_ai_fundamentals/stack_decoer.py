"""
stack_decoder.py — CLI tool that classifies a GenAI use case across the deployment stack.

Calls gpt-5.4-mini with a structured prompt and validates the response via Pydantic
before formatting and printing a classification report.
"""

import os
from dotenv import load_dotenv
import json
import argparse

from openai import OpenAI

from models import StackClassification


def load_env() -> str:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env")
    return api_key

def build_prompt(use_case: str) -> str:
    return f"""You are a Kubernetes and Generative AI solutions architect.

A user has described the following GenAI use case:
\"{use_case}\"

Classify this use case across the GenAI deployment stack and respond with a JSON object containing exactly these fields:

- deployment_layer: one of "prompt_engineering", "rag", "fine_tuning", or "foundation_model"
- k8s_resources: a list of Kubernetes resource types this workload would require
- complexity: one of "low", "medium", or "high"
- estimated_cost_tier: one of "low", "medium", or "high"
- reasoning: a two to three sentence explanation of your classification

Respond with valid JSON only. No markdown, no backticks, no explanation outside the JSON object."""

def classify_use_case(use_case: str, api_key: str) -> StackClassification:
    """
    Call the OpenAI API and return a validated StackClassification.
    """
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You are a Kubernetes and Generative AI solutions architect."},
            {"role": "user", "content": build_prompt(use_case)}
        ],
        # Be more deterministic
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    # Verify the response matches the Pydantic model
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}\nRaw response: {raw}")
    
    return StackClassification(**data)

def format_report(use_case: str, result: StackClassification) -> str:
    """
    Format the Pydantic classification result as a human readable CLI report
    """
    k8s_resources = "\n".join(f"  - {r}" for r in result.k8s_resources)

    return f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║              GenAI Stack Decoder — Classification Report     ║
    ╚══════════════════════════════════════════════════════════════╝

    Use Case:
    {use_case}

    Deployment Layer:
    {result.deployment_layer}

    Kubernetes Resources Required:
    {k8s_resources}

    Complexity:       {result.complexity}
    Cost Tier:        {result.estimated_cost_tier}

    Reasoning:
    {result.reasoning}
    """

def main():
    """
    Parse the use case aurgument and run the classification pipeline
    """
    parser = argparse.ArgumentParser(
        description="Classify a GenAI use case acceoss the deployment stack"
    )
    parser.add_argument(
        "use_case",
        type=str,
        help="A description of your GenAI use case in plain language"
    )
    args = parser.parse_args()

    api_key = load_env()
    result = classify_use_case(args.use_case, api_key)
    report = format_report(args.use_case, result)
    print(report)

if __name__ == "__main__":
    main()
