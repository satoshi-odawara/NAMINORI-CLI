import subprocess
import json
import pytest
import os
import numpy as np

def run_script(input_dict):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "run_iso_10816.py")
    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_dict))
    return process.returncode, stdout, stderr

def test_integration_accuracy():
    # 100Hz sine, 10mm/s velocity amp
    # Theory: Disp Peak-to-Peak = 2 * (10 / (2 * pi * 100)) * 1000 = 31.83 um
    fs = 5000
    t = np.linspace(0, 1.0, fs, endpoint=False)
    v_signal = 10.0 * np.sin(2 * np.pi * 100 * t)
    
    input_data = {
        "equipment_id": "TEST_SINE",
        "signal": v_signal.tolist(),
        "fs": fs
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    disp_p2p = result["features"]["displacement_p2p_um"]
    
    # Check if calculated p2p is within 5% of theory (31.83 um)
    assert abs(disp_p2p - 31.83) < (31.83 * 0.05)
    assert result["features"]["iso_10816_zone"] == "B" # 25 < 31.8 < 50

def test_error_handling():
    input_data = {"fs": 1000} # Missing signal
    rc, stdout, stderr = run_script(input_data)
    assert rc == 1
    err = json.loads(stderr)
    assert err["status"] == "error"
    assert "Missing signal" in err["message"]
