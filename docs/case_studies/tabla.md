# Case Study: Tabla Fine-Tuning

## Data
- Source: 1.5 hours of tabla recordings
- Selection: 51 clips (90-110s) curated for variety
- Annotation: 2 descriptors (tempo, energy)

## Training
- Model: acestep-v15-base
- Adapter: DoRA (rank 128, alpha 240)
- Epochs: 300, Batch Size: 2
- Loss Weighting: min_snr, CFG Dropout: 0.45
- Hardware: RTX 3090 (24GB) on RunPod
- Time: ~37 minutes

## Results
- Loss: 0.5765 → 0.2173 (62.3% reduction)
- Before/After spectrograms
- Sample audio outputs

## Lessons Learned
1. Quality > Quantity: 51 good clips > 200 noisy clips
2. Caption consistency matters: structured descriptors work
3. DoRA > LoRA for timbre learning
4. min_snr loss weighting stabilizes training on base models
5. Trigger word (`tablastyle`) is essential for style control

## Next Steps
- Apply same methodology to bansuri
- Experiment with stem separation for mixed-instrument recordings
- Compare DoRA vs LoRA vs LoKR
