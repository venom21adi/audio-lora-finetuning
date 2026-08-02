#!/usr/bin/env python3
"""
Generate before/after audio for comparison.
Requires: ACE-Step installed, LoRA weights available.
"""

import os
import subprocess
from pathlib import Path

PROMPTS = [
    "tablastyle, fast tabla solo with energetic strokes",
    "tablastyle, slow meditative tabla with deep bass",
    "tablastyle, tabla solo with complex patterns",
    "tablastyle, tabla with finger rolls and embellishments",
    "tablastyle, tabla solo in Teental, moderate tempo",
]

CHECKPOINT_DIR = "/path/to/ACE-Step-1.5/checkpoints"
ADAPTER_PATH = "/path/to/tabla_lora_run1_20260801_1011/final"
OUTPUT_DIR = "./results/tabla/audio"

def generate(prompt, adapter=None, output_name="output"):
    """Generate audio with optional adapter."""
    cmd = [
        "uv", "run", "sidestep", "generate",
        "--checkpoint-dir", CHECKPOINT_DIR,
        "--model", "acestep-v15-base",
        "--prompt", prompt,
        "--duration", "30",
        "--output", f"{OUTPUT_DIR}/{output_name}.wav"
    ]
    if adapter:
        cmd += ["--adapter", adapter]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    os.makedirs(f"{OUTPUT_DIR}/before", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/after", exist_ok=True)

    for i, prompt in enumerate(PROMPTS):
        # Base model
        generate(prompt, output_name=f"before/prompt_{i+1}")
        # With adapter
        generate(prompt, adapter=ADAPTER_PATH, output_name=f"after/prompt_{i+1}")
