# Infrastructure Setup

This document outlines the infrastructure used for training and inference. The setup is optimized for **cost, performance, and reproducibility**.

---

## 1. GPU Instance

| Spec | Value |
|------|-------|
| GPU | NVIDIA RTX 3090 (24GB VRAM) |
| CPU | 8 vCPUs |
| RAM | 32GB |
| Storage | 80GB SSD |
| Platform | RunPod (spot pricing) |

**Why this configuration:**
- 24GB VRAM comfortably fits the 4B DiT + DoRA (~6GB peak)
- 8 vCPUs handle data preprocessing efficiently
- Spot pricing keeps cost low (~$0.44/hr)

---

## 2. Software Stack

| Component | Purpose |
|-----------|---------|
| **ACE-Step 1.5** | Base model + inference engine |
| **Side-Step** | Training framework with corrected timestep sampling |
| **UV** | Fast Python dependency management |
| **PyTorch 2.10** | Deep learning framework (CUDA 12.8) |
| **Flash Attention 2** | Memory-efficient attention |
| **Hugging Face Hub** | Model downloads |

**Installation (on RunPod):**

```bash
# Clone repositories
git clone https://github.com/ACE-Step/ACE-Step-1.5.git
git clone https://github.com/koda-dernet/Side-Step.git

# Install dependencies
cd ACE-Step-1.5 && uv sync
cd ../Side-Step && uv sync

# Download base model (auto-downloads via ACE-Step UI)
uv run acestep --share
