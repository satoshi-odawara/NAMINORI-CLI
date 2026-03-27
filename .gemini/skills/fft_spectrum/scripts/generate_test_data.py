import numpy as np
import pandas as pd
import os

def generate_signal(fs, duration, freqs, amplitudes, noise_level=0.1):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.zeros_like(t)
    for f, a in zip(freqs, amplitudes):
        signal += a * np.sin(2 * np.pi * f * t)
    signal += noise_level * np.random.randn(len(t))
    return t, signal

def save_to_csv(path, t, signal):
    df = pd.DataFrame({'time': t, 'amplitude': signal})
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

fs = 1000
duration = 1.0
base_dir = ".gemini/skills/fft_spectrum/assets/synthetic"

# Normal: 10Hz, Amp=1.0
t, sig_normal = generate_signal(fs, duration, [10], [1.0])
save_to_csv(os.path.join(base_dir, "normal.csv"), t, sig_normal)

# Fault 1X: 10Hz, Amp=2.5 (Unbalance)
t, sig_1x = generate_signal(fs, duration, [10], [2.5])
save_to_csv(os.path.join(base_dir, "fault_1x.csv"), t, sig_1x)

# Fault 2X: 10Hz, Amp=1.0 + 20Hz, Amp=1.5 (Misalignment)
t, sig_2x = generate_signal(fs, duration, [10, 20], [1.0, 1.5])
save_to_csv(os.path.join(base_dir, "fault_2x.csv"), t, sig_2x)
