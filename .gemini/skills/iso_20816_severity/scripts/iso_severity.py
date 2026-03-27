import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

# ISO 20816-3:2009 Thresholds [mm/s]
THRESHOLD_TABLE = {
    "group1": {"rigid": [2.3, 4.5, 7.1], "flexible": [3.5, 7.1, 11.0]},
    "group2": {"rigid": [1.4, 2.8, 4.5], "flexible": [2.3, 4.5, 7.1]},
    "group3": {"rigid": [2.3, 4.5, 7.1], "flexible": [3.5, 7.1, 11.0]},
    "group4": {"rigid": [1.4, 2.8, 4.5], "flexible": [2.3, 4.5, 7.1]},
}

def get_zone(rms, thresholds):
    if rms <= thresholds[0]: return "A"
    if rms <= thresholds[1]: return "B"
    if rms <= thresholds[2]: return "C"
    return "D"

def run_severity(input_data):
    try:
        signal = input_data.get("signal")
        fs = input_data.get("fs")
        equipment_id = input_data.get("equipment_id", "unknown")
        meta = input_data.get("metadata", {})
        
        group = str(meta.get("equipment_group", "group2")).lower()
        support = str(meta.get("support_type", "rigid")).lower()

        if group not in THRESHOLD_TABLE or support not in ["rigid", "flexible"]:
            raise ValueError(f"Invalid equipment_group or support_type: {group}, {support}")

        # Calculate RMS if signal is provided, else use pre-calculated RMS from metadata
        if signal is not None:
            rms_val = np.sqrt(np.mean(np.array(signal)**2))
        else:
            rms_val = meta.get("rms_value")
            if rms_val is None:
                raise ValueError("Missing 'signal' or 'metadata.rms_value'.")

        thresholds = THRESHOLD_TABLE[group][support]
        zone = get_zone(rms_val, thresholds)
        
        status_map = {"A": "normal", "B": "normal", "C": "warning", "D": "alert"}
        status = status_map[zone]

        # Visualization
        plt.figure(figsize=(8, 4))
        zones = ["A", "B", "C", "D"]
        colors = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
        y_max = max(rms_val * 1.5, thresholds[2] * 1.2)
        
        # Plot thresholds as background colors
        plt.axhspan(0, thresholds[0], color=colors[0], alpha=0.3, label="Zone A")
        plt.axhspan(thresholds[0], thresholds[1], color=colors[1], alpha=0.3, label="Zone B")
        plt.axhspan(thresholds[1], thresholds[2], color=colors[2], alpha=0.3, label="Zone C")
        plt.axhspan(thresholds[2], y_max, color=colors[3], alpha=0.3, label="Zone D")
        
        plt.bar([equipment_id], [rms_val], color="#34495e", width=0.5, label="Current RMS")
        plt.ylabel("Velocity RMS [mm/s]")
        plt.title(f"ISO 20816-3 Severity - {equipment_id} ({group}, {support})")
        plt.legend(loc='upper right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Standard visualization path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rel_plot_dir = "assets/plots"
        abs_plot_dir = os.path.join(os.path.dirname(__file__), "..", rel_plot_dir)
        os.makedirs(abs_plot_dir, exist_ok=True)
        
        plot_filename = f"{equipment_id}_iso_severity_{timestamp}.png"
        abs_plot_path = os.path.join(abs_plot_dir, plot_filename)
        # Relative path from root for output JSON
        rel_plot_path = f".gemini/skills/iso_20816_severity/assets/plots/{plot_filename}"
        
        plt.savefig(abs_plot_path)
        plt.close()

        output = {
            "status": status,
            "score": float(rms_val),
            "method": "iso_20816_severity",
            "features": {
                "rms": float(rms_val),
                "zone": zone,
                "thresholds": thresholds,
                "plot_url": rel_plot_path
            },
            "threshold": {
                "basis": f"ISO 20816-3:2009 {group} {support}",
                "value": thresholds
            },
            "message": f"ISO Zone: {zone}. RMS value: {rms_val:.2f} mm/s. Support: {support}. Group: {group}."
        }
        return output

    except Exception as e:
        error_json = {
            "status": "error",
            "error_code": "MATH_ERROR" if isinstance(e, ZeroDivisionError) else "INVALID_PARAM",
            "message": str(e),
            "suggestion": "Check equipment_group (group1-4) and support_type (rigid|flexible)."
        }
        sys.stderr.write(json.dumps(error_json, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        result = run_severity(input_json)
        print(json.dumps(result, indent=2))
    except Exception as e:
        error_json = {
            "status": "error",
            "error_code": "INVALID_FORMAT",
            "message": "Failed to parse input JSON.",
            "suggestion": "Provide valid JSON through stdin."
        }
        sys.stderr.write(json.dumps(error_json, ensure_ascii=False))
        sys.exit(1)
