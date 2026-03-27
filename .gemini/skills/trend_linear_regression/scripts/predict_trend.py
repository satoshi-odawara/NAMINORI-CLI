import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.stats import linregress

def predict_trend(input_data):
    try:
        history = input_data.get("history", [])
        threshold = input_data.get("threshold_value")
        equipment_id = input_data.get("equipment_id", "unknown")

        if len(history) < 2:
            raise ValueError("Insufficient data points for trend analysis. Minimum 2 required.")
        if threshold is None:
            raise ValueError("Threshold value must be specified.")

        # Convert timestamps to numeric (seconds from first entry)
        times = []
        values = []
        base_time = datetime.strptime(history[0]['timestamp'], "%Y-%m-%d %H:%M:%S")
        
        for entry in history:
            t = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
            diff_sec = (t - base_time).total_seconds()
            times.append(diff_sec)
            values.append(entry['rms_value'])

        x = np.array(times)
        y = np.array(values)

        # Linear regression: y = slope * x + intercept
        res = linregress(x, y)
        slope = res.slope
        intercept = res.intercept
        r_squared = res.rvalue**2

        # Predict when threshold will be reached
        status = "normal"
        message = "Trend analysis completed."
        predicted_date_str = "N/A"
        rul_days = -1

        if slope > 0:
            target_sec = (threshold - intercept) / slope
            if target_sec > x[-1]:
                predicted_time = base_time + timedelta(seconds=target_sec)
                predicted_date_str = predicted_time.strftime("%Y-%m-%d")
                rul_days = (predicted_time - datetime.now()).days
                
                if rul_days < 30: status = "warning"
                if rul_days < 7: status = "alert"
            else:
                message = "Threshold already exceeded according to trend."
                status = "alert"
        else:
            message = "Trend is stable or decreasing. No threshold hit predicted."

        # Visualization
        plt.figure(figsize=(10, 5))
        plt.plot(x/86400, y, 'o', label='Actual Measurements')
        
        # Plot regression line
        x_pred = np.linspace(0, max(x[-1], (threshold - intercept) / slope if slope > 0 else x[-1]*1.2), 100)
        y_pred = slope * x_pred + intercept
        plt.plot(x_pred/86400, y_pred, '--', color='red', label=f'Trend (R2={r_squared:.2f})')
        
        plt.axhline(y=threshold, color='orange', linestyle=':', label=f'Threshold ({threshold})')
        plt.title(f"Vibration Trend Prediction - {equipment_id}")
        plt.xlabel("Days from start")
        plt.ylabel("RMS Value")
        plt.legend()
        plt.grid(True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_trend_{timestamp}.png"
        abs_plot_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "plots")
        os.makedirs(abs_plot_dir, exist_ok=True)
        plot_path = os.path.join(abs_plot_dir, plot_filename)
        plt.savefig(plot_path)
        plt.close()

        output = {
            "status": status,
            "score": float(r_squared),
            "method": "trend_linear_regression",
            "features": {
                "slope": float(slope),
                "intercept": float(intercept),
                "r_squared": float(r_squared),
                "predicted_threshold_date": predicted_date_str,
                "remaining_useful_life_days": int(rul_days),
                "plot_url": f".gemini/skills/trend_linear_regression/assets/plots/{plot_filename}"
            },
            "threshold": {"value": threshold, "basis": "ISO User defined"},
            "message": f"{message} Predicted threshold date: {predicted_date_str}. RUL: {rul_days} days."
        }
        return output

    except Exception as e:
        err = {
            "status": "error",
            "error_code": "COMPUTATION_FAILED",
            "message": str(e),
            "suggestion": "Check input data format and ensure at least 2 points exist."
        }
        sys.stderr.write(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(predict_trend(input_json), indent=2))
    except Exception:
        sys.exit(1)
