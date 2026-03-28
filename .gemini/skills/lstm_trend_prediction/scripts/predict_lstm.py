import torch
import torch.nn as nn
import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class LSTMModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=16, num_layers=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

def run_prediction(input_data):
    try:
        equipment_id = input_data.get("equipment_id", "unknown")
        history = input_data.get("history", [])
        threshold = input_data.get("threshold_value")
        horizon = input_data.get("metadata", {}).get("horizon_days", 30)

        models_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
        config_path = os.path.join(models_dir, f"{equipment_id}_config.json")
        model_path = os.path.join(models_dir, f"{equipment_id}_lstm.pth")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Model not found for {equipment_id}.")

        with open(config_path, "r") as f:
            config = json.load(f)
        
        seq_length = config["seq_length"]
        max_val = config["max_val"]

        if len(history) < seq_length:
            raise ValueError(f"Need at least {seq_length} points for prediction.")

        # Prepare initial sequence
        recent_values = [h['rms_value'] for h in history[-seq_length:]]
        current_sequence = np.array(recent_values) / max_val
        
        model = LSTMModel()
        model.load_state_dict(torch.load(model_path, weights_only=True))
        model.eval()

        predictions = []
        rul_days = -1
        
        # Recursive prediction
        input_seq = torch.FloatTensor(current_sequence).view(1, seq_length, 1)
        for i in range(horizon):
            with torch.no_grad():
                pred = model(input_seq)
                pred_val = pred.item()
                predictions.append(pred_val * max_val)
                
                if (pred_val * max_val) >= threshold and rul_days == -1:
                    rul_days = i + 1
                
                # Update input_seq
                new_val = torch.FloatTensor([[[pred_val]]])
                input_seq = torch.cat((input_seq[:, 1:, :], new_val), dim=1)

        # Visualization
        plt.figure(figsize=(10, 5))
        past_x = np.arange(len(history))
        past_y = [h['rms_value'] for h in history]
        plt.plot(past_x, past_y, label='Actual')
        
        future_x = np.arange(len(history), len(history) + horizon)
        plt.plot(future_x, predictions, '--', color='red', label='LSTM Prediction')
        
        plt.axhline(y=threshold, color='orange', linestyle=':', label='Threshold')
        plt.title(f"LSTM Trend Prediction - {equipment_id}")
        plt.legend()
        plt.grid(True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_lstm_trend_{timestamp}.png"
        abs_plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", "plots", plot_filename)
        os.makedirs(os.path.dirname(abs_plot_path), exist_ok=True)
        plt.savefig(abs_plot_path); plt.close()

        status = "normal"
        if 0 < rul_days < 30: status = "warning"
        if 0 < rul_days < 7: status = "alert"

        return {
            "status": status,
            "method": "lstm_trend_prediction",
            "features": {
                "predicted_values": [float(v) for v in predictions],
                "remaining_useful_life_days": int(rul_days),
                "plot_url": f".gemini/skills/lstm_trend_prediction/assets/plots/{plot_filename}"
            },
            "message": f"LSTM Prediction: {status.upper()}. Estimated RUL: {rul_days} days."
        }

    except Exception as e:
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_prediction(input_json), indent=2))
    except Exception:
        sys.exit(1)
