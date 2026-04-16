from pydantic import BaseModel
from typing import List


class StackClassification(BaseModel):
    deployment_layer: str
    k8s_resources: List[str]
    complexity: str
    estimated_cost_tier: str
    reasoning: str