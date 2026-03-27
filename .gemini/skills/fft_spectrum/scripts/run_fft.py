import numpy as np
import pandas as pd
import json
import sys
import os
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import get_window

def run_fft(input_data):
    try:
        signal = np.array(input_data.get("signal"))
        fs = input_data.get("fs")
        window_name = input_data.get("metadata", {}).get("window", "hann")
        equipment_id = input_data.get("equipment_id", "unknown")

        if signal is None or fs is None:
            raise ValueError("Missing signal or fs in input data.")

        n = len(signal)
        # Apply window
        win = get_window(window_name, n)
        windowed_signal = signal * win
        
        # Scaling factor for window (Amplitude recovery)
        scaling_factor = n / np.sum(win)
        
        # FFT
        yf = fft(windowed_signal)
        xf = fftfreq(n, 1/fs)[:n//2]
        
        # Magnitude Spectrum (0-peak)
        psd = 2.0/n * np.abs(yf[0:n//2]) * scaling_factor
        
        # Find dominant frequencies (Top 3)
        peak_indices = np.argsort(psd)[-3:][::-1]
        peak_freqs = xf[peak_indices].tolist()
        peak_amps = psd[peak_indices].tolist()
        
        dominant_freq = peak_freqs[0]
        max_amp = peak_amps[0]

        # Visualization
        plt.figure(figsize=(10, 4))
        plt.plot(xf, psd)
        plt.title(f"FFT Spectrum - {equipment_id} ({window_name} window)")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude")
        plt.grid(True)
        
        plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", f"fft_plot_{equipment_id}.png")
        plt.savefig(plot_path)
        plt.close()

        # Output Schema
        output = {
            "status": "normal",
            "score": float(max_amp), # Using max amplitude as a simple score for now
            "method": "fft_spectrum",
            "features": {
                "frequencies": xf.tolist(),
                "psd": psd.tolist(),
                "peak_frequencies": peak_freqs,
                "peak_amplitudes": peak_amps,
                "dominant_frequency": dominant_freq,
                "plot_url": plot_path
            },
            "threshold": {
                "basis": "Maximum amplitude of dominant frequency",
                "value": 2.0 # Placeholder
            },
            "message": f"Dominant frequency detected at {dominant_freq:.2f} Hz with amplitude {max_amp:.4f}."
        }
        
        # Alert logic (Example)
        if max_amp > 2.0:
            output["status"] = "warning"
            output["message"] += " High vibration amplitude detected."

        return output

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    # Standard input from stdin (JSON)
    try:
        input_json = json.load(sys.stdin)
        result = run_fft(input_json)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
