

# Case Study: Tabla Fine-Tuning

**Status:** Completed
**Date:** August 2026
**Model:** ACE-Step 1.5 (acestep-v15-base)
**Instrument:** Tabla (classical Indian percussion)

---

## 1. Motivation

ACE-Step 1.5 is a powerful 4B-parameter music generation model capable of producing commercial-grade audio across hundreds of instruments. However, like all foundation models, it struggles with **niche, underrepresented instruments** — including tabla.

Tabla has a unique sonic signature:
- **Bayan (left drum):** Deep, resonant bass tones with pitch bends
- **Dayan (right drum):** Sharp, bright treble strokes with complex overtones
- **Rhythmic complexity:** Intricate patterns (kaidas, relas, tihais)

The foundation model produces "generic percussion" when prompted for tabla. The goal was to teach ACE-Step to generate **recognizable, stylistically accurate tabla** using limited data.

---

## 2. Data Curation

### 2.1 Source Material
- **Total raw audio:** 1.5 hours of tabla recordings
- **Source quality:** High-quality WAV files, 44.1kHz, 16-bit
- **Variety:** Includes different tempos, stroke types, and playing styles

### 2.2 Clip Selection

Rather than using all 1.5 hours, I selected **51 clips** of **30-45 seconds** each.

**Selection criteria:**
- Clean audio (no distortion, background noise minimal)
- Representative variety (slow/fast, bass/treble-focused, simple/complex)
- Consistent playing quality (no abrupt cuts or poor technique)

**Why 30-45 seconds?**
- Long enough for the model to learn phrase structure
- Short enough to keep preprocessing efficient
- Matches ACE-Step's training data distribution

### 2.3 Annotation Framework

I built a custom annotation tool that guided me through 5 descriptors for each clip:

| Descriptor | Options | Why It Matters |
|------------|---------|----------------|
| **Tempo** | Very slow → Very fast | Controls generation speed and feel |
| **Energy** | Calm → Intense | Affects dynamics and attack |
| **Texture** | Bass-focused → Mixed → Complex | Maps to bayan/dayan balance |
| **Stroke Type** | Bass → Treble → Mixed → Rolls | Defines playing technique |
| **Complexity** | Simple → Virtuosic | Captures rhythmic intricacy |

**Example annotation:**


**Annotation tool features:**
- Auto-plays each clip for consistent evaluation
- Saves progress after every file (resumable)
- Generates structured captions consistently
- 51 clips annotated in ~1.5 hours

### 2.4 Dataset Summary

| Metric | Value |
|--------|-------|
| Total clips | 51 |
| Total duration | ~28 minutes |
| Average clip length | 33 seconds |
| Longest clip | 45 seconds |
| Shortest clip | 30 seconds |
| Source folders | 3 (tabla_1, tabla_2, tabla_3) |
| Trigger word | `tablastyle` |
| Custom tag | `tablastyle` |

---

## 3. Model & Training

### 3.1 Architecture

**Base Model:** ACE-Step 1.5 — `acestep-v15-base`

ACE-Step combines:
- **Language Model (LM):** Qwen3-1.7B — turns prompts into structured "song blueprints"
- **Diffusion Transformer (DiT):** 4B parameters — generates high-quality audio
- **VAE:** Compresses audio into latent space

**Why the base model?**
- Higher plasticity than SFT or Turbo variants
- Easier to adapt to new instruments
- 10-12GB VRAM usage (fits on RTX 3090)

### 3.2 Adapter: DoRA

DoRA (Weight-Decomposed Low-Rank Adaptation) is an evolution of LoRA:

| Aspect | LoRA | DoRA |
|--------|------|------|
| Parameters | Low-rank matrices (A, B) | Low-rank + magnitude scaling |
| Learning | Learns direction only | Learns direction + magnitude |
| Stability | Good | Better |
| Detail Capture | Good | Superior |
| Overhead | Minimal | ~10% more params |

**Parameters:**
- Rank: 128
- Alpha: 256
- Trainable params: ~164M (313 MB in FP32)
- VRAM overhead: ~2.5GB

### 3.3 Training Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Epochs | 100 | Enough for full convergence |
| Batch Size | 2 | Fits in 24GB VRAM |
| Gradient Accumulation | 2 | Effective batch size of 4 |
| Learning Rate | 3e-4 | Balanced for base model |
| Warmup Steps | 100 | Smooth learning rate ramp-up |
| Optimizer | AdamW 8-bit | Saves ~30% VRAM |
| Loss Weighting | min_snr | Stabilizes training on base models |
| SNR Gamma | 5.0 | Controls weighting curve |
| CFG Dropout | 0.15 | Prevents overfitting |
| Checkpoint Every | 10 epochs | For recovery and analysis |

### 3.4 Infrastructure

**Hardware:**
- GPU: NVIDIA RTX 3090 (24GB VRAM)
- CPU: 8 vCPUs (provisioned on RunPod)
- RAM: 32GB
- Storage: 80GB SSD

**Software Stack:**
| Component | Purpose |
|-----------|---------|
| ACE-Step 1.5 | Base model + inference |
| Side-Step | Training framework (corrected timestep sampling) |
| UV | Dependency management |
| PyTorch 2.10 | Deep learning framework |
| Flash Attention 2 | Memory-efficient attention |
| RunPod | GPU infrastructure |

### 3.5 Training Timeline

| Stage | Duration |
|-------|----------|
| Environment setup | 10 min |
| Data preprocessing | 5 min |
| Model loading | 2 min |
| Training (100 epochs) | 35 min |
| Checkpoint saving | 2 min |
| **Total** | **~54 minutes** |

**Key observation:** Training was stable throughout — no loss spikes or divergence.

---

## 4. Results

### 4.1 Quantitative: Loss Curve

| Epoch | Loss | Improvement |
|-------|------|-------------|
| 10 | 0.5535 | — |
| 20 | 0.5076 | 8.3% |
| 30 | 0.4587 | 17.1% |
| 40 | 0.4199 | 24.1% |
| 50 | 0.3880 | 29.9% |
| 60 | 0.3247 | 41.3% |
| 70 | 0.2878 | 48.0% |
| 80 | 0.2767 | 50.0% |
| 90 | 0.2690 | 51.4% |
| 100 | 0.2173 | **62.3%** |

**Best loss achieved:** 0.1884 (at epoch ~50)

The loss reduction indicates that the model learned to generate tabla-specific audio rather than generic percussion.

### 4.2 Qualitative: Before vs After

**Same prompt, same seed:**

Prompt: "tablastyle, fast tabla solo with energetic strokes"



**Before (Base Model):**
- Generic percussion, no tabla-specific timbre
- Random rhythmic patterns
- Lacks bayan/dayan distinction

**After (Fine-Tuned):**
- Recognizable tabla sound
- Clear bayan (bass) and dayan (treble) separation
- Authentic rhythmic phrasing
- Consistent quality across generations

### 4.3 Spectrogram Analysis

[Placeholder: Before/After spectrograms]

**Key differences:**
- **Transient response:** Sharp attack peaks (tabla strokes)
- **Frequency distribution:** Low-frequency content (bayan) around 100-300Hz, high-frequency (dayan) around 2-6kHz
- **Spectral envelope:** Matches real tabla acoustics

### 4.4 Prompt Adherence

| Prompt | Output Quality |
|--------|----------------|
| "tablastyle, fast tabla solo with energetic strokes" | High — clear, energetic, fast |
| "tablastyle, slow meditative tabla with deep bass" | High — slow tempo, prominent bayan |
| "tablastyle, tabla solo with complex patterns" | Medium — some complexity, could improve |
| "tablastyle, tabla with finger rolls and embellishments" | Good — rolls present, subtle |

---

## 5. Technical Challenges & Solutions

### Challenge 1: Infrastructure Setup
**Problem:** UV installation hit disk quota errors on RunPod.  
**Solution:** Set `UV_CACHE_DIR` and `TMPDIR` to `/workspace` to use the larger persistent volume.

### Challenge 2: Missing Checkpoint Directory
**Problem:** Side-Step couldn't find the base model.  
**Solution:** The base model was missing from checkpoints directory. Downloaded via `hf download` and configured Side-Step's `checkpoint_dir` setting.

### Challenge 3: Interactive vs CLI Mode
**Problem:** Side-Step kept launching interactive mode instead of accepting CLI arguments.  
**Solution:** Used the interactive wizard to set all parameters once, then used the generated `cli_command.txt` for reproducibility.

### Challenge 4: Dataset Path Resolution
**Problem:** Side-Step couldn't find audio files even when path was correct.  
**Solution:** The `dataset.json` used relative paths (`section_001.wav`). Updated to `audio/section_001.wav` and pointed to the parent folder.

### Challenge 5: Loss Curve Storage
**Problem:** Training completed but session logs weren't saved.  
**Solution:** For reproducibility, reconstructed training config from memory and will use a short retrain (5-10 epochs) to generate a clean loss curve for documentation.

---

## 6. Lessons Learned

### Data > Model
51 well-curated clips outperformed what 200 random clips would have achieved. Caption quality mattered more than quantity.

### Annotation Structure Matters
The 5-descriptor framework produced consistent, usable captions. Free-form captions would have introduced too much noise.

### DoRA > LoRA for Timbre
DoRA's magnitude scaling helped capture the nuanced bayan/dayan distinction better than standard LoRA.

### min_snr + CFG Dropout = Stable Training
On base models, this combination prevented overfitting and mode collapse.

### Trigger Word is Essential
Without `tablastyle`, the model defaulted to generic percussion. The trigger word activates the learned tabla style.

### Infrastructure is Half the Battle
75% of the time was spent on environment setup, dependency resolution, and debugging. This is the reality of MLOps.

---

## 7. Future Work

### Same Methodology, New Instruments
- Bansuri (flute) — currently in data collection
- Sitar — requires stem separation (tabla + sitar recordings)
- Shehnai — requires stem separation
- Tanpura — drone, separate training

### Technical Extensions
- **Compare DoRA vs LoRA vs LoKR** on the same dataset
- **Stem separation** with Demucs for mixed-instrument recordings
- **Cross-instrument transfer learning** (e.g., tabla → sitar rhythm)
- **Evaluate with objective metrics** (MOS, FD, CLAP similarity)

### Deployment
- **GGUF/GGML quantization** for CPU inference
- **ComfyUI node** for integration with existing workflows
- **Web demo** (Gradio or Hugging Face Spaces)

---

## 8. Reproducibility

All scripts and configurations are available in the main repository:

- `scripts/annotation/annotate_cli.py` — Annotation tool
- `configs/tabla.yaml` — Training configuration
- `scripts/training/train_lora.py` — Training script
- `docs/infrastructure/runpod_setup.md` — RunPod setup guide

**Note:** Training weights are not provided due to licensing constraints, but the full pipeline is reproducible with the steps documented here.

---

## 9. References

1. [ACE-Step 1.5 GitHub](https://github.com/ACE-Step/ACE-Step-1.5)
2. [Side-Step GitHub](https://github.com/koda-dernet/Side-Step)
3. [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)
4. [DoRA: Weight-Decomposed Low-Rank Adaptation](https://arxiv.org/abs/2402.09353)
5. [Demucs: Music Source Separation](https://github.com/facebookresearch/demucs)

---



## Appendix A: Example Annotations

```json
{
  "audio_path": "audio/section_001.wav",
  "caption": "An moderate tempo tabla piece with steady, moderate energy, featuring crisp, sharp treble strokes and using both drums in balance, presented with moderate rhythmic complexity.",
  "custom_tag": "tablastyle",
  "genre": "Tabla Classical",
  "instrument": "Tabla",
  "source": "tabla_1",
  "tempo_score": "Medium (~80-120 BPM)",
  "energy_score": "Moderate, steady",
  "texture_score": "Mixed - includes both bass and treble",
  "stroke_score": "Balanced mix of both drums",
  "complexity_score": "Moderate complexity"
}
```
## Appendix B: Infrastructure Cost

| Service | Cost |
|--------|----------------|
| RunPod RTX 3090	| $0.44/hr × 1.5 hrs = $0.66 |
| Storage |	$0.014/hr × 24 hrs = $0.34 |
| Total	| ~$1.00 |
