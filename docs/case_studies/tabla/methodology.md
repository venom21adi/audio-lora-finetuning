# Methodology: Fine-Tuning Niche Instruments

This document outlines the core principles behind fine-tuning large music models on underrepresented instruments with limited data. The approach is intentionally **data-first** and **infrastructure-conscious**.

---

## 1. Data Philosophy: Quality Over Quantity

Foundation models like ACE-Step are already trained on massive datasets. The goal of fine-tuning is **not to teach the model music** — it's to **teach it a specific timbre and style**.

With that in mind:

- **51 clips (30–45 seconds each)** were sufficient for learning tabla.
- **Clean, consistent audio** mattered more than volume.
- **Diversity** (tempo, energy) was prioritized over repetition.

**Key takeaway:** A small, well-curated dataset outperforms a large, noisy one.

---

## 2. Annotation Strategy: Structured Descriptors

Free-form captions introduce inconsistency. Instead, I used a **structured framework** with 5 descriptors:

| Descriptor | Purpose |
|------------|---------|
| **Tempo** | Controls generation speed |
| **Energy** | Affects dynamics and intensity |


These descriptors were consistent across all 51 clips, ensuring the model learned a **structured representation** of tabla rather than random associations.

---

## 3. Training Approach: DoRA + min_snr + CFG Dropout

### DoRA over LoRA

DoRA (Weight-Decomposed Low-Rank Adaptation) adds magnitude scaling to standard LoRA. This helps capture **timbre nuances** that are critical for instruments like tabla — where the bass/treble distinction is essential.

**DoRA parameters:**
- Rank: 128
- Alpha: 240
- Trainable params: ~164M

### min_snr Loss Weighting

Base models are sensitive to noise. `min_snr` loss weighting stabilizes training by dynamically adjusting the loss contribution of each timestep. This prevented overfitting and mode collapse.

### CFG Dropout

A 25% dropout during Classifier-Free Guidance prevents the model from becoming too dependent on the prompt, improving generalization and reducing artifacts.

---

## 4. Evaluation: Loss + Listening

### Quantitative: Loss Curve

Loss decreased from **0.5765 to 0.2173** (62.3% reduction). The curve was stable with no divergence.

### Qualitative: Listening Tests

The fine-tuned model produces:
- Recognizable tabla timbre (bayan + dayan separation)
- Authentic rhythmic phrasing
- Consistent quality across prompts

**The trigger word `tablastyle` is essential** — without it, the model defaults to generic percussion.

---

## 5. Key Takeaways

1. **Data curation > data volume.** 51 good clips beat 500 average ones.
2. **Structured annotation reduces noise.** Consistent descriptors produce cleaner learning.
3. **DoRA captures instrument-specific timbre.** Useful for percussion and melodic instruments.
4. **min_snr + CFG dropout = stable training** on base models.
5. **Infrastructure matters.** The right tools (Side-Step, UV, RunPod) make the difference between success and frustration.

---

## 6. Applicability

This methodology is not specific to tabla. It applies to any niche instrument where:
- Limited data is available
- Timbre and style matter more than raw composition
- Foundation models exist but lack the specific capability

**Next case studies** (bansuri, sitar, shehnai) will follow the same framework.
