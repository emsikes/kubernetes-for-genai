# Kubernetes for Generative AI Solutions

![Python](https://img.shields.io/badge/python-3.11.9-blue)
![Kubernetes](https://img.shields.io/badge/kubernetes-EKS-orange)
![License](https://img.shields.io/badge/license-MIT-green)

Code-along project repository for *Kubernetes for Generative AI Solutions*
by Ashok Srirama and Sukirti Gupta (Packt, 2025).

One mini-project per chapter.

---

## Environment

| Component | Detail |
|---|---|
| OS | Windows 11 + WSL2 (Ubuntu) |
| Python | 3.11.9 via pyenv |
| Cluster | Amazon EKS + Proxmox homelab |
| GPU | NVIDIA RTX / Google Colab Pro (H100/A100) |
| Venv | Single shared `.venv` at repo root |

---

## Setup

```bash
git clone <repo-url>
cd k8s-genai-solutions

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your API keys in .env
```

---

## Chapter Index

| Chapter | Title | Mini-Project | Environment |
|---|---|---|---|
| 01 | Generative AI Fundamentals | GenAI Stack Decoder CLI | Local |
| 02 | Kubernetes — Introduction and Integration with GenAI | GenAI Container — Local First | Local / Docker |
| 03 | Getting Started with Kubernetes in the Cloud | EKS Cluster + First LLM Deployment | EKS |
| 04 | GenAI Model Optimization for Domain-Specific Use Cases | RAG Pipeline on K8s | EKS |
| 05 | Working with GenAI on K8s — Chatbot Example | Fine-Tuning Job + RAG Chatbot Full Stack | EKS + Colab |
| 06 | Scaling GenAI Applications on Kubernetes | Autoscaling Under Load | EKS |
| 07 | Cost Optimization of GenAI Applications on Kubernetes | Kubecost + Goldilocks Right-Sizing | EKS |
| 08 | Networking Best Practices for Deploying GenAI on K8s | Network Policy Enforcement | EKS |
| 09 | Security Best Practices for Deploying GenAI on Kubernetes | Defense-in-Depth Hardening | EKS |
| 10 | Optimizing GPU Resources for GenAI Applications | GPU Time-Slicing + DCGM Monitoring | Local / WSL2 |
| 11 | GenAIOps — Data Management and GenAI Automation Pipeline | KubeRay Pipeline + MLflow Tracking | Proxmox |
| 12 | Observability — Getting Visibility into GenAI on K8s | Full LGTM Stack + LangFuse Tracing | Proxmox |
| 13 | High Availability and Disaster Recovery | Multi-AZ Resilience + Chaos Test | EKS |
| 14 | Wrapping Up — GenAI Coding Assistants | AI-Assisted K8s Ops CLI | Local |

---

## Repository Structure

```
k8s-genai-solutions/
├── .env                   # API keys — never committed
├── .env.example           # Safe template to commit
├── .gitignore
├── README.md
├── requirements.txt       # Shared venv for all chapters
├── ch01_genai_fundamentals/
├── ch02_k8s_genai_intro/
├── ch03_eks_cluster_setup/
├── ch04_model_optimization/
├── ch05_chatbot_k8s/
├── ch06_scaling/
├── ch07_cost_optimization/
├── ch08_networking/
├── ch09_security/
├── ch10_gpu_optimization/
├── ch11_genaiops_pipelines/
├── ch12_observability/
├── ch13_ha_dr/
└── ch14_coding_assistants/
```
