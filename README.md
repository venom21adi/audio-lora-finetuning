# Audio LoRA Fine-Tuning

> A systematic framework for fine-tuning large music generation models on niche instruments with limited data.

## Overview

This repository documents the methodology, infrastructure, and results of fine-tuning [ACE-Step 1.5](https://github.com/ACE-Step/ACE-Step-1.5) — a 4B-parameter DiT-based music model — on **niche, underrepresented instruments** using limited data (30–60 minutes per instrument).

**Current Case Study:** Tabla (completed)  
**Planned:** Bansuri, Sitar, Shehnai, Tanpura

## Why This Matters

| Problem | Solution |
|---------|----------|
| Foundation models don't understand niche instruments | LoRA fine-tuning with 30–60 min of audio |
| Mixed-instrument recordings (tabla + sitar) | Stem separation with Demucs |
| Inconsistent captioning | Custom annotation tool with structured descriptors |
| Reproducibility | Documented pipeline + configs |
| Resource constraints | Optimized for RTX 3090 (24GB) |

## Technical Stack

- **Model:** ACE-Step 1.5 (4B DiT) — `acestep-v15-base`
- **Adapter:** DoRA (rank 128, alpha 240)
- **Framework:** Side-Step (corrected timestep sampling + CFG dropout)
- **Infrastructure:** RunPod (RTX 3090, 24GB VRAM)
- **Data Tools:** Custom annotation CLI, Demucs for stem separation
- **Analysis:** Loss curves, spectrograms, frequency analysis

## Key Technical Contributions

1. **Data Curation Pipeline** — From raw recordings to annotated, preprocessed tensors
2. **Annotation Framework** — Structured descriptors (tempo, energy) for consistent captioning
3. **Training Optimization** — DoRA + min_snr loss + CFG dropout = stable, high-quality learning
4. **Infrastructure as Code** — Reproducible RunPod setup with UV and Side-Step
5. **Comparative Analysis** — Before/after spectrograms and other relevant metrics

## Results (Tabla Case Study)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Loss | 0.5765 | 0.2173 | **62.3%** |
| Timbre Accuracy | Generic percussion | Tabla-specific (bayan/dayan) | Qualitative |
| Trigger Word | None | `tablastyle` | Enables style control |

### Sample Output


## Project Structure

See [docs/methodology.md] for detailed walkthroughs.

## Reproducibility

Every case study includes:
- `configs/<instrument>.yaml` — exact hyperparameters
- `scripts/` — annotation, analysis
- `docs/case_studies/instrument` — methodology and infrastructure

## License

MIT

## Acknowledgments

- [ACE-Step](https://github.com/ACE-Step/ACE-Step-1.5) — Foundation model
- [Side-Step](https://github.com/koda-dernet/Side-Step) — Training framework
- [RunPod](https://runpod.io) — GPU infrastructure
