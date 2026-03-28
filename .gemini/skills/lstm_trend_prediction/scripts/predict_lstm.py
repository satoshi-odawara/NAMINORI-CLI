import torch
import torch.nn as nn
import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

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

def run_prediction(input_data):
    try:
        equipment_id = input_data.get("equipment_id", "unknown")
        history = input_data.get("history", [])
        threshold = input_data.get("threshold_value")
        horizon = input_data.get("metadata", {}).get("horizon_days", 60)

        models_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
        config_path = os.path.join(models_dir, f"{equipment_id}_config.json")
        model_path = os.path.join(models_dir, f"{equipment_id}_lstm.pth")

        with open(config_path, "r") as f:
            config = json.load(f)
        
        seq_length = config["seq_length"]
        scale_factor = config["scale_factor"]

        # Prepare initial sequence
        recent_values = [h['rms_value'] for h in history[-seq_length:]]
        current_sequence = np.array(recent_values) / scale_factor
        
        model = LSTMModel()
        model.load_state_dict(torch.load(model_path, weights_only=True))
        model.eval()

        predictions = []
        rul_days = -1
        input_seq = torch.FloatTensor(current_sequence).view(1, seq_length, 1)
        
        for i in range(horizon):
            with torch.no_grad():
                pred = model(input_seq)
                pred_val = pred.item()
                actual_pred = pred_val * scale_factor
                predictions.append(actual_pred)
                
                if actual_pred >= threshold and rul_days == -1:
                    rul_days = i + 1
                
                new_val = torch.FloatTensor([[[pred_val]]])
                input_seq = torch.cat((input_seq[:, 1:, :], new_val), dim=1)

        # Visualization
        plt.figure(figsize=(10, 5))
        past_y = [h['rms_value'] for h in history]
        plt.plot(np.arange(len(past_y)), past_y, label='Actual')
        plt.plot(np.arange(len(past_y), len(past_y) + horizon), predictions, '--', label='LSTM')
        plt.axhline(y=threshold, color='red', linestyle=':', label='Threshold')
        plt.title(f"LSTM Trend - {equipment_id}")
        plt.legend(); plt.grid(True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_lstm_{timestamp}.png"
        plt.savefig(os.path.join(os.path.dirname(__file__), "..", "assets", "plots", plot_filename))
        plt.close()

        return {
            "status": "warning" if 0 < rul_days < 30 else "normal",
            "features": {
                "predicted_values": [float(v) for v in predictions],
                "remaining_useful_life_days": int(rul_days),
                "plot_url": f".gemini/skills/lstm_trend_prediction/assets/plots/{plot_filename}"
            },
            "message": f"Estimated RUL: {rul_days} days."
        }

    except Exception as e:
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_prediction(input_json), indent=2))
    except Exception: sys.exit(1)
