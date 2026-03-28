import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import json
import sys
import os

torch.manual_seed(42)

class LSTMModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=32, num_layers=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        xs.append(data[i:(i + seq_length)])
        ys.append(data[i + seq_length])
    return np.array(xs), np.array(ys)

def train_lstm(csv_path, equipment_id, seq_length=10):
    try:
        df = pd.read_csv(csv_path)
        values = df['rms_value'].values.astype(np.float32)
        
        # Scaling: Use a fixed headroom for prediction
        # Let's use a simple scaling: value / 20.0 (assuming max threshold is 15-20)
        scale_factor = 20.0
        scaled_values = values / scale_factor
        
        X, y = create_sequences(scaled_values, seq_length)
        X = torch.FloatTensor(X).unsqueeze(-1)
        y = torch.FloatTensor(y).unsqueeze(-1)

        model = LSTMModel()
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.005)

        for epoch in range(300):
            model.train()
            optimizer.zero_grad()
            output = model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()

        models_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
        os.makedirs(models_dir, exist_ok=True)
        torch.save(model.state_dict(), os.path.join(models_dir, f"{equipment_id}_lstm.pth"))
        
        config = {
            "seq_length": seq_length,
            "scale_factor": float(scale_factor)
        }
        with open(os.path.join(models_dir, f"{equipment_id}_config.json"), "w") as f:
            json.dump(config, f)

        print(json.dumps({"status": "success", "loss": float(loss.item())}))

    except Exception as e:
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    train_lstm(sys.argv[1], sys.argv[2])
