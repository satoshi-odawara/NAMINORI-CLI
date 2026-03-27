import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew

def extract_time_features(input_data):
    try:
        signal = np.array(input_data.get("signal"))
        fs = input_data.get("fs")
        equipment_id = input_data.get("equipment_id", "unknown")

        if signal is None:
            raise ValueError("Missing signal in input data.")

        # Basic statistics
        mean_val = np.mean(signal)
        std_val = np.std(signal)
        rms_val = np.sqrt(np.mean(signal**2))
        peak_val = np.max(np.abs(signal))
        peak_to_peak = np.max(signal) - np.min(signal)
        
        # Crest Factor
        crest_factor = peak_val / rms_val if rms_val > 0 else 0
        
        # Kurtosis and Skewness (Fisher's definition: normal distribution = 0)
        # We will add 3.0 to Kurtosis to match the Pearson definition if needed, 
        # but let's stick to Fisher (excess kurtosis) and clarify in SKILL.md.
        kurt_val = kurtosis(signal) 
        skew_val = skew(signal)

        # Visualization (Time domain plot)
        plt.figure(figsize=(10, 4))
        plt.plot(signal)
        plt.title(f"Time Domain Signal - {equipment_id}")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.grid(True)
        
        plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", f"time_plot_{equipment_id}.png")
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plt.close()

        # Threshold logic (Example)
        status = "normal"
        message = f"Time domain features extracted for {equipment_id}."
        
        if kurt_val > 3.0: # High excess kurtosis (>3.0 above normal)
            status = "warning"
            message += " High Kurtosis detected (possible impact noise/bearing fault)."
        elif rms_val > 5.0:
            status = "warning"
            message += " High RMS value detected (possible unbalance/looseness)."

        # Output Schema
        output = {
            "status": status,
            "score": float(rms_val),
            "method": "time_domain_features",
            "features": {
                "rms": float(rms_val),
                "peak": float(peak_val),
                "peak_to_peak": float(peak_to_peak),
                "crest_factor": float(crest_factor),
                "kurtosis": float(kurt_val), # Fisher's excess kurtosis
                "skewness": float(skew_val),
                "mean": float(mean_val),
                "std": float(std_val),
                "plot_url": plot_path
            },
            "threshold": {
                "kurtosis_limit": 3.0,
                "rms_limit": 5.0
            },
            "message": message
        }

        return output

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        result = extract_time_features(input_json)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
