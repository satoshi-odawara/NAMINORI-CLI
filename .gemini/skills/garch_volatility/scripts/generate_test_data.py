import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

def save_vols(path, values):
    base_date = datetime(2026, 1, 1)
    dates = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(len(values))]
    df = pd.DataFrame({'timestamp': dates, 'rms_value': values})
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

base_dir = ".gemini/skills/garch_volatility/assets/synthetic"
n_points = 200

# Stable: Constant variance
stable_values = 2.0 + 0.1 * np.random.randn(n_points)
save_vols(os.path.join(base_dir, "stable_vol.csv"), stable_values)

# Burst: Sudden increase in variance at point 150
burst_values = 2.0 + 0.1 * np.random.randn(n_points)
burst_values[150:] += 0.8 * np.random.randn(n_points - 150)
save_vols(os.path.join(base_dir, "burst_vol.csv"), burst_values)
