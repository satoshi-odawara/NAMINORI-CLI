import torch
import torch.nn as nn
import numpy as np
import json
import sys
import os

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
        return self.decoder(self.encoder(x))

def run_inference(input_data):
    try:
        equipment_id = input_data.get("equipment_id", "unknown")
        features = input_data.get("metadata", {}).get("features", {})
        
        models_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
        config_path = os.path.join(models_dir, f"{equipment_id}_config.json")
        model_path = os.path.join(models_dir, f"{equipment_id}_ae.pth")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"No trained model found for {equipment_id}.")

        with open(config_path, "r") as f:
            config = json.load(f)
        
        input_vec = []
        for col in config["columns"]:
            val = features.get(col)
            if val is None:
                raise ValueError(f"Feature column '{col}' missing.")
            input_vec.append(float(val))
        
        input_tensor = torch.FloatTensor([input_vec])
        
        model = Autoencoder(config["input_dim"])
        model.load_state_dict(torch.load(model_path, weights_only=True))
        model.eval()

        with torch.no_grad():
            reconstructed = model(input_tensor)
            mse = float(torch.mean((reconstructed - input_tensor)**2).item())

        threshold = float(config["threshold"])
        status = "normal"
        if mse > threshold:
            status = "alert"

        output = {
            "status": status,
            "score": float(mse / threshold) if threshold > 0 else 0.0,
            "method": "autoencoder_anomaly",
            "features": {
                "reconstruction_error": mse,
                "threshold": threshold,
                "anomaly_ratio": float(mse / threshold)
            },
            "message": f"Anomaly detection: {status.upper()}. Error: {mse:.4f} (Threshold: {threshold:.4f})"
        }
        return output

    except Exception as e:
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_inference(input_json), indent=2))
    except Exception:
        sys.exit(1)
