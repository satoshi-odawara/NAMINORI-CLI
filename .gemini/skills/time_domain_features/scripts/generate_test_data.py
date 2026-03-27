import numpy as np
import pandas as pd
import os

def save_to_csv(path, signal):
    df = pd.DataFrame({'amplitude': signal})
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

fs = 1000
duration = 1.0
n = int(fs * duration)
t = np.linspace(0, duration, n, endpoint=False)
base_dir = ".gemini/skills/time_domain_features/assets/synthetic"

# Normal: Gaussian noise
sig_normal = np.random.normal(0, 1.0, n)
save_to_csv(os.path.join(base_dir, "normal.csv"), sig_normal)

# Unbalance: Large sine wave (10Hz) + small noise
sig_unbalance = 5.0 * np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(n)
save_to_csv(os.path.join(base_dir, "unbalance.csv"), sig_unbalance)

# Bearing Fault: Gaussian noise + sparse high-amplitude pulses
sig_bearing = np.random.normal(0, 0.5, n)
pulse_indices = np.random.choice(n, 20, replace=False)
sig_bearing[pulse_indices] += 10.0 * (np.random.choice([1, -1], 20))
save_to_csv(os.path.join(base_dir, "bearing_fault.csv"), sig_bearing)
