import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

def save_trend(path, values):
    base_date = datetime(2026, 1, 1)
    dates = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(len(values))]
    df = pd.DataFrame({'timestamp': dates, 'rms_value': values})
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

base_dir = ".gemini/skills/lstm_trend_prediction/assets/synthetic"
n_points = 150

# Normal: Slow linear increase
normal_values = np.linspace(1.0, 2.0, n_points) + 0.05 * np.random.randn(n_points)
save_trend(os.path.join(base_dir, "normal_linear.csv"), normal_values)

# Fault: Exponential increase (Accelerating degradation)
t = np.linspace(0, 10, n_points)
fault_values = 1.0 + 0.1 * np.exp(0.4 * t) + 0.1 * np.random.randn(n_points)
save_trend(os.path.join(base_dir, "fault_exponential.csv"), fault_values)
