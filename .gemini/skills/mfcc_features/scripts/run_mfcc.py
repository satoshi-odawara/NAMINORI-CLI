import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

try:
    import librosa
    import librosa.display
except ImportError:
    err = {
        "status": "error",
        "error_code": "DEPENDENCY_MISSING",
        "message": "The 'librosa' library is required for MFCC features.",
        "suggestion": "Please run: pip install librosa"
    }
    sys.stderr.write(json.dumps(err, ensure_ascii=False))
    sys.exit(1)

def run_mfcc(input_data):
    try:
        signal = np.array(input_data.get("signal"))
        fs = input_data.get("fs")
        equipment_id = input_data.get("equipment_id", "unknown")
        meta = input_data.get("metadata", {})
        
        n_mfcc = meta.get("n_mfcc", 13)
        n_fft = meta.get("n_fft", 2048)
        hop_length = meta.get("hop_length", 512)

        if signal is None or fs is None:
            raise ValueError("Missing signal or fs in input data.")

        # Extract MFCCs
        # librosa expects float signal
        signal = signal.astype(float)
        mfccs = librosa.feature.mfcc(y=signal, sr=fs, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
        
        # Calculate statistics for the segment
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)

        # Visualization: MFCC Spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfccs, x_axis='time', sr=fs, hop_length=hop_length)
        plt.colorbar()
        plt.title(f"MFCC Spectrogram - {equipment_id}")
        plt.ylabel("MFCC Coefficients")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_mfcc_{timestamp}.png"
        abs_plot_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "plots")
        os.makedirs(abs_plot_dir, exist_ok=True)
        plot_path = os.path.join(abs_plot_dir, plot_filename)
        plt.savefig(plot_path)
        plt.close()

        output = {
            "status": "normal",
            "score": 0.0, # Placeholder
            "method": "mfcc_features",
            "features": {
                "mfcc_coefficients": mfccs.tolist(),
                "mfcc_mean": mfcc_mean.tolist(),
                "mfcc_std": mfcc_std.tolist(),
                "n_mfcc": n_mfcc,
                "plot_url": f".gemini/skills/mfcc_features/assets/plots/{plot_filename}"
            },
            "threshold": {},
            "message": f"Extracted {n_mfcc} MFCC features. Mean values represent the spectral envelope."
        }
        return output

    except Exception as e:
        err = {
            "status": "error",
            "error_code": "COMPUTATION_FAILED",
            "message": str(e),
            "suggestion": "Check signal format and sampling frequency."
        }
        sys.stderr.write(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    try:
        input_json = json.load(sys.stdin)
        print(json.dumps(run_mfcc(input_json), indent=2))
    except Exception:
        sys.exit(1)
