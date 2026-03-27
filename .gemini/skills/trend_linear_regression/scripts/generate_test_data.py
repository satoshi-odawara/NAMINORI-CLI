import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

def save_trend(path, values):
    base_date = datetime(2026, 3, 1)
    dates = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(len(values))]
    df = pd.DataFrame({'timestamp': dates, 'rms_value': values})
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

base_dir = ".gemini/skills/trend_linear_regression/assets/synthetic"
n_days = 30

# Normal: Low level, random fluctuation
normal_values = 1.0 + 0.1 * np.random.randn(n_days)
save_trend(os.path.join(base_dir, "normal_trend.csv"), normal_values)

# Fault: Linear increase from 1.0 to 6.0
fault_values = np.linspace(1.0, 6.0, n_days) + 0.2 * np.random.randn(n_days)
save_trend(os.path.join(base_dir, "fault_trend.csv"), fault_values)

# Insufficient: Only 3 points
save_trend(os.path.join(base_dir, "insufficient_data.csv"), [1.0, 1.1, 1.2])
