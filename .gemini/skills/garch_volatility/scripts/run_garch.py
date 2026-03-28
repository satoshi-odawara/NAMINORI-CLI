import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

try:
    from arch import arch_model
except ImportError:
    # Rule §6.4: Standard error JSON
    err = {
        "status": "error",
        "error_code": "DEPENDENCY_MISSING",
        "message": "The 'arch' library is required for this skill.",
        "suggestion": "Please run: pip install arch"
    }
    sys.stderr.write(json.dumps(err, ensure_ascii=False))
    sys.exit(1)

def run_garch(input_data):
    try:
        history = input_data.get("history", [])
        equipment_id = input_data.get("equipment_id", "unknown")
        unit = input_data.get("metadata", {}).get("unit", "unknown")

        if len(history) < 50: # GARCH usually needs more data
            raise ValueError("Insufficient data points. GARCH analysis requires at least 50 historical points.")

        values = np.array([h['rms_value'] for t, h in enumerate(history)])
        
        # GARCH(1,1) Model
        # vol='Garch', p=1, q=1
        model = arch_model(values, vol='Garch', p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        
        # Conditional Volatility (standard deviation)
        cond_vol = res.conditional_volatility
        current_vol = cond_vol[-1]
        mean_vol = np.mean(cond_vol)

        # Status logic: Is current volatility significantly higher than average?
        status = "normal"
        if current_vol > 2.0 * mean_vol:
            status = "warning"
        if current_vol > 4.0 * mean_vol:
            status = "alert"

        # Visualization
        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(values, label='Measured RMS', alpha=0.5, color='gray')
        ax1.set_ylabel(f'Value [{unit}]')
        
        ax2 = ax1.twinx()
        ax2.plot(cond_vol, label='GARCH Volatility', color='tab:red', linewidth=2)
        ax2.set_ylabel('Volatility (StdDev)')
        
        plt.title(f"GARCH Volatility Analysis - {equipment_id}")
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.grid(True, alpha=0.3)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_garch_{timestamp}.png"
        abs_plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", "plots", plot_filename)
        os.makedirs(os.path.dirname(abs_plot_path), exist_ok=True)
        plt.savefig(abs_plot_path)
        plt.close()

        output = {
            "status": status,
            "score": float(current_vol / mean_vol) if mean_vol > 0 else 0.0,
            "method": "garch_volatility",
            "features": {
                "current_volatility": float(current_vol),
                "average_volatility": float(mean_vol),
                "volatility_history": cond_vol.tolist(),
                "plot_url": f".gemini/skills/garch_volatility/assets/plots/{plot_filename}",
                "unit": unit
            },
            "threshold": {
                "basis": "Relative increase in conditional variance",
                "warning_limit": 2.0,
                "alert_limit": 4.0
            },
            "message": f"Stability assessment: {status.upper()}. Current instability factor is {current_vol/mean_vol:.2f}x of historical average."
        }
        return output

    except Exception as e:
        err = {
            "status": "error",
            "error_code": "MATH_ERROR",
            "message": str(e),
            "suggestion": "Check input data. Ensure measurements are stationary or use returns."
        }
        sys.stderr.write(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_garch(input_json), indent=2))
    except Exception:
        sys.exit(1)
