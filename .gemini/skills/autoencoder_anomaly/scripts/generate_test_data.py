import numpy as np
import pandas as pd
import os

def generate_features(n_samples, anomaly_ratio=0.0):
    # Base: 15 dimensional feature vector (13 MFCCs + RMS + Kurtosis)
    # Mean and scale roughly matching real world stats
    base_mean = np.zeros(15)
    base_std = 0.5 * np.ones(15)
    
    data = np.random.normal(base_mean, base_std, (n_samples, 15))
    
    is_anomaly = np.zeros(n_samples)
    if anomaly_ratio > 0:
        n_anomalies = int(n_samples * anomaly_ratio)
        anomaly_indices = np.random.choice(n_samples, n_anomalies, replace=False)
        # Anomalies have shifted mean or higher variance
        data[anomaly_indices] += 3.0 * np.random.choice([-1, 1], (n_anomalies, 15))
        is_anomaly[anomaly_indices] = 1
        
    cols = [f'mfcc_{i}' for i in range(13)] + ['rms', 'kurtosis']
    df = pd.DataFrame(data, columns=cols)
    if anomaly_ratio > 0:
        df['is_anomaly'] = is_anomaly
    return df

base_dir = ".gemini/skills/autoencoder_anomaly/assets/synthetic"

# Train: 500 normal samples
train_df = generate_features(500, anomaly_ratio=0.0)
train_df.to_csv(os.path.join(base_dir, "train_normal.csv"), index=False)

# Test: 100 samples (10% anomalies)
test_df = generate_features(100, anomaly_ratio=0.1)
test_df.to_csv(os.path.join(base_dir, "test_mixed.csv"), index=False)

print(f"Generated synthetic features in {base_dir}")
