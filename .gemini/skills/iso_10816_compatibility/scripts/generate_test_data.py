import numpy as np
import pandas as pd
import os

def generate_velocity_signal(fs, duration, freq, velocity_amp_mms):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # Velocity signal in mm/s
    signal = velocity_amp_mms * np.sin(2 * np.pi * freq * t)
    # Add some noise
    signal += 0.1 * np.random.randn(len(t))
    return t, signal

fs = 5000
duration = 1.0
base_dir = ".gemini/skills/iso_10816_compatibility/assets/synthetic"

# Test Case: 100Hz, 10mm/s velocity amplitude
t, sig = generate_velocity_signal(fs, duration, 100, 10.0)
df = pd.DataFrame({'time': t, 'velocity_mms': sig})
df.to_csv(os.path.join(base_dir, "test_velocity_100hz.csv"), index=False)
print(f"Saved: test_velocity_100hz.csv")
