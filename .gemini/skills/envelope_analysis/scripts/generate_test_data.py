import numpy as np
import pandas as pd
import os

def generate_bearing_fault(fs, duration, fault_freq, resonance_freq, noise_level=0.1):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # Generate repetitive impacts at fault_freq
    impacts = np.zeros_like(t)
    impact_spacing = int(fs / fault_freq)
    impact_indices = np.arange(0, len(t), impact_spacing)
    
    # Each impact excites a high frequency resonance
    for idx in impact_indices:
        # Exponentially decaying sine wave as impact response
        decay_t = np.linspace(0, 0.01, int(fs * 0.01)) # 10ms decay
        if idx + len(decay_t) < len(t):
            impact_response = np.exp(-500 * decay_t) * np.sin(2 * np.pi * resonance_freq * decay_t)
            impacts[idx:idx+len(decay_t)] += impact_response

    signal = impacts + noise_level * np.random.randn(len(t))
    return t, signal

fs = 10000 # Higher fs for resonance
duration = 1.0
base_dir = ".gemini/skills/envelope_analysis/assets/synthetic"

# BPFO Fault: ~105Hz impacts
t, sig_bpfo = generate_bearing_fault(fs, duration, 105, 2000)
df = pd.DataFrame({'time': t, 'amplitude': sig_bpfo})
df.to_csv(os.path.join(base_dir, "fault_bpfo.csv"), index=False)
print(f"Saved: fault_bpfo.csv")

# Normal: Gaussian noise only
sig_normal = 0.1 * np.random.randn(int(fs * duration))
df_normal = pd.DataFrame({'time': t, 'amplitude': sig_normal})
df_normal.to_csv(os.path.join(base_dir, "normal.csv"), index=False)
print(f"Saved: normal.csv")
