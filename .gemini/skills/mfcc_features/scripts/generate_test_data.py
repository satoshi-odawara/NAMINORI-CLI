import numpy as np
import pandas as pd
import os

def generate_audio_like(fs, duration, freqs, amps):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        signal += a * np.sin(2 * np.pi * f * t)
    signal += 0.05 * np.random.randn(len(t))
    return signal

fs = 22050
duration = 1.0
base_dir = ".gemini/skills/mfcc_features/assets/synthetic"

# Normal: Low freqs
sig_normal = generate_audio_like(fs, duration, [60, 120, 300], [1.0, 0.5, 0.2])
pd.DataFrame({'amplitude': sig_normal}).to_csv(os.path.join(base_dir, "normal_hum.csv"), index=False)

# Fault: High freq squeal
sig_fault = generate_audio_like(fs, duration, [60, 120, 3000], [1.0, 0.5, 0.8])
pd.DataFrame({'amplitude': sig_fault}).to_csv(os.path.join(base_dir, "fault_squeal.csv"), index=False)

print(f"Generated test data in {base_dir}")
