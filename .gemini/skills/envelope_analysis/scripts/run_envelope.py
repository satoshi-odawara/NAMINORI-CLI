import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, filtfilt

def run_envelope(input_data):
    try:
        signal = np.array(input_data.get("signal"))
        fs = input_data.get("fs")
        equipment_id = input_data.get("equipment_id", "unknown")
        bearing_params = input_data.get("metadata", {}).get("bearing_params", {})
        
        if signal is None or fs is None:
            raise ValueError("Missing signal or fs in input data.")

        # 1. Bandpass Filter (Optional: focus on resonance band)
        # For simplicity, let's assume high-frequency bandpass is pre-applied or focus on raw for now
        # Standard: focus on 1kHz - 5kHz if resonance exists
        nyq = 0.5 * fs
        low = 500 / nyq
        high = 4000 / nyq
        if high >= 1.0: high = 0.99
        b, a = butter(4, [low, high], btype='band')
        filtered_signal = filtfilt(b, a, signal)

        # 2. Hilbert Transform (Envelope extraction)
        analytic_signal = hilbert(filtered_signal)
        amplitude_envelope = np.abs(analytic_signal)
        
        # Remove DC component (mean) for better spectrum visualization
        amplitude_envelope -= np.mean(amplitude_envelope)

        # 3. FFT of Envelope
        n = len(amplitude_envelope)
        yf = np.fft.fft(amplitude_envelope)
        xf = np.fft.fftfreq(n, 1/fs)[:n//2]
        psd_envelope = 2.0/n * np.abs(yf[0:n//2])

        # 4. Theoretical Defect Frequencies (simplified)
        # fr: shaft freq, n: balls, d: ball diam, D: pitch diam
        fr = bearing_params.get("fr", 0)
        theory_bpfo = 0
        if fr > 0:
            # Typical BPFO is ~3.5 to 4.5 * fr
            theory_bpfo = bearing_params.get("n", 8) * fr / 2 * (1 - bearing_params.get("d_D_ratio", 0.2))
        
        # 5. Peak Finding in Envelope Spectrum
        dominant_idx = np.argsort(psd_envelope)[-5:][::-1]
        peak_freqs = xf[dominant_idx].tolist()
        peak_amps = psd_envelope[dominant_idx].tolist()

        # Visualization
        plt.figure(figsize=(12, 5))
        plt.subplot(2, 1, 1)
        plt.plot(signal[:1000]) # Zoomed signal
        plt.title(f"Time Waveform (Zoom) - {equipment_id}")
        plt.subplot(2, 1, 2)
        plt.plot(xf, psd_envelope)
        plt.title(f"Envelope Spectrum - {equipment_id}")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Envelope Amp")
        plt.xlim(0, 500) # Bearings faults are usually in low freq
        plt.grid(True)
        
        plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", f"envelope_plot_{equipment_id}.png")
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plt.close()

        # Alert Logic
        status = "normal"
        message = "Envelope analysis completed."
        if theory_bpfo > 0:
            # Check if any peak is near theory_bpfo (within 5%)
            for pf in peak_freqs:
                if abs(pf - theory_bpfo) / theory_bpfo < 0.05:
                    status = "alert"
                    message = f"Defect frequency detected at {pf:.2f} Hz (Theory BPFO: {theory_bpfo:.2f} Hz)."
                    break

        output = {
            "status": status,
            "score": float(np.max(psd_envelope)),
            "method": "envelope_analysis",
            "features": {
                "envelope_frequencies": xf.tolist(),
                "envelope_spectrum": psd_envelope.tolist(),
                "peak_frequencies": peak_freqs,
                "theory_bpfo": float(theory_bpfo),
                "plot_url": plot_path
            },
            "threshold": {
                "basis": "Proximity to theoretical bearing defect frequencies",
                "margin": 0.05
            },
            "message": message
        }
        return output

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        result = run_envelope(input_json)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
