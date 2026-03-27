import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import detrend
from datetime import datetime

def run_iso_10816(input_data):
    try:
        raw_signal = input_data.get("signal")
        fs = input_data.get("fs")
        equipment_id = input_data.get("equipment_id", "unknown")
        
        if raw_signal is None or fs is None:
            raise ValueError("Missing signal or fs.")
            
        v_signal = np.array(raw_signal)
        n = len(v_signal)
        v_signal = detrend(v_signal)

        # Frequency domain integration (more stable for displacement)
        vf = fft(v_signal)
        xf = fftfreq(n, 1/fs)
        
        # Integration in freq domain: D(f) = V(f) / (j * 2 * pi * f)
        # Avoid division by zero at f=0
        df = np.zeros_like(vf, dtype=complex)
        indices = np.where(xf != 0)
        df[indices] = vf[indices] / (1j * 2 * np.pi * xf[indices])
        
        # Apply low-cut filter in freq domain (e.g., 10Hz)
        low_cut = 10.0
        df[np.abs(xf) < low_cut] = 0
        
        disp = np.real(ifft(df))
        
        # Convert to µm
        disp_um = disp * 1000.0
        
        # Features
        v_rms = np.sqrt(np.mean(v_signal**2))
        disp_p2p = np.max(disp_um) - np.min(disp_um)

        # ISO 10816 Zones (Class II default)
        status = "normal"; zone = "A"
        if disp_p2p > 80: status = "alert"; zone = "D"
        elif disp_p2p > 50: status = "warning"; zone = "C"
        elif disp_p2p > 25: status = "normal"; zone = "B"

        # Visualization
        plt.figure(figsize=(10, 4))
        plt.plot(disp_um, label="Displacement [µm]", color='tab:red')
        plt.title(f"Displacement Waveform (Freq-Domain Integration) - {equipment_id}")
        plt.grid(True); plt.legend()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_iso10816_{timestamp}.png"
        abs_plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", "plots", plot_filename)
        os.makedirs(os.path.dirname(abs_plot_path), exist_ok=True)
        plt.savefig(abs_plot_path); plt.close()

        return {
            "status": status,
            "score": float(disp_p2p),
            "method": "iso_10816_compatibility",
            "features": {
                "velocity_rms_mms": float(v_rms),
                "displacement_p2p_um": float(disp_p2p),
                "iso_10816_zone": zone,
                "plot_url": f".gemini/skills/iso_10816_compatibility/assets/plots/{plot_filename}"
            },
            "message": f"ISO 10816 Zone {zone}. P-P: {disp_p2p:.1f} µm."
        }

    except Exception as e:
        sys.stderr.write(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_iso_10816(input_json), indent=2))
    except Exception:
        sys.exit(1)
