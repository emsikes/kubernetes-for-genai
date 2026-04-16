# Ch01 — Generative AI Fundamentals

## Pattern
Structured LLM classification of GenAI use cases across the deployment stack.

## Mini-Project
**GenAI Stack Decoder CLI** — a command-line tool that takes a plain-language
GenAI use case description and classifies it across four deployment layers,
identifying required Kubernetes resources, complexity, cost tier, and
architectural reasoning.

## Implementation
| File | Purpose |
|---|---|
| `models.py` | Pydantic model defining the structured classification output |
| `stack_decoder.py` | CLI tool — five functions wired into an argparse entrypoint |

## Key Concepts
- The four GenAI deployment layers: `prompt_engineering`, `rag`, `fine_tuning`,
  `foundation_model`
- Structured JSON output from an LLM enforced via Pydantic validation
- Root `.env` loading pattern used across all chapters
- Low temperature (0.2) for deterministic classification tasks
- The K8s resource vocabulary grows with deployment complexity — prompt
  engineering needs only a handful of resources; fine-tuning requires
  isolation, stateful storage, and network controls

## Test Cases
| Use Case | Layer | Complexity |
|---|---|---|
| Documentation chatbot | `rag` | medium |
| Email summarization via API | `prompt_engineering` | low |
| Custom medical diagnosis model | `fine_tuning` | high |

## How to Run
```bash
cd k8s-genai-solutions
source .venv/bin/activate
python ch01_genai_fundamentals/stack_decoder.py "<your use case description>"
```

## Observations
The model correctly scales the Kubernetes resource list with deployment
complexity. Fine-tuning use cases produced Namespace, StatefulSet, and
NetworkPolicy — resources driven by data sensitivity and compute requirements
rather than just application serving needs.