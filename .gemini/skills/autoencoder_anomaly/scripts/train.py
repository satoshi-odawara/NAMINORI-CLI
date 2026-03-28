import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import json
import sys
import os

# Set seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)

class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def train_model(csv_path, equipment_id):
    try:
        df = pd.read_csv(csv_path)
        data = df.drop(columns=['is_anomaly'], errors='ignore').values
        
        input_dim = data.shape[1]
        model = Autoencoder(input_dim)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)

        tensor_data = torch.FloatTensor(data)
        for epoch in range(100):
            model.train()
            optimizer.zero_grad()
            output = model(tensor_data)
            loss = criterion(output, tensor_data)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            reconstructed = model(tensor_data)
            errors = torch.mean((reconstructed - tensor_data)**2, dim=1).numpy()
            # FIX: Ensure float type for JSON serialization
            threshold = float(np.percentile(errors, 99))

        models_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
        os.makedirs(models_dir, exist_ok=True)
        torch.save(model.state_dict(), os.path.join(models_dir, f"{equipment_id}_ae.pth"))
        
        config = {
            "input_dim": int(input_dim),
            "threshold": threshold,
            "columns": df.drop(columns=['is_anomaly'], errors='ignore').columns.tolist()
        }
        with open(os.path.join(models_dir, f"{equipment_id}_config.json"), "w") as f:
            json.dump(config, f)

        print(json.dumps({
            "status": "success",
            "message": f"Model trained for {equipment_id}",
            "threshold": threshold,
            "input_dim": int(input_dim)
        }))

    except Exception as e:
        # Rule §6.4: Standard error JSON
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    train_model(sys.argv[1], sys.argv[2])
