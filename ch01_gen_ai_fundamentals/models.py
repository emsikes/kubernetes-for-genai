"""
Pydantic schema for the GenAI Stack Decoder.

This will validate that the LLM response confirms with this exact schema
before it's passed downstream to the rest of the program.  If the model
returns a wrong type or unexptected value, Pydantic will raise a ValidationError
from here rather than lettting it propogate silently.
"""

from pydantic import BaseModel
from typing import List


class StackClassification(BaseModel):
    """
    Structured classification of a GenAI use case accross the four
    layers of the GenAI deployment stack.

    - deployment_layer: Which layer of the stack this use case lives in.
      One of:
        * prompt_engineering
        * rag
        * fine_tuning
        * foundation_model
    - k8s_resources: The K8s resource types this workload requires
    - complexity: Overall implmentation complexity - low, medium, high
    - estimated_cost_tier: Relative infrastructure cost estimate - low, medium, high
    - reasoning: The model's explanation of its classification decision 
    """
    deployment_layer: str
    k8s_resources: List[str]
    complexity: str
    estimated_cost_tier: str
    reasoning: str