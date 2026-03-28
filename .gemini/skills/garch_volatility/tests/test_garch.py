import subprocess
import json
import pytest
import os
import pandas as pd

def run_script(input_dict):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "run_garch.py")
    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_dict))
    return process.returncode, stdout, stderr

def test_volatility_burst():
    # Load burst volatility data (Variance increase at end)
    csv_path = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "burst_vol.csv")
    df = pd.read_csv(csv_path)
    history = df.to_dict('records')
    
    input_data = {
        "equipment_id": "TEST_BURST",
        "history": history,
        "metadata": {"unit": "mms"}
    }
    
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    
    # Conditional volatility should be higher at the end
    cond_vol = result["features"]["volatility_history"]
    assert cond_vol[-1] > cond_vol[0] * 2.0
    assert result["status"] in ["warning", "alert"]

def test_stable_volatility():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "stable_vol.csv")
    df = pd.read_csv(csv_path)
    history = df.to_dict('records')
    
    input_data = {
        "equipment_id": "TEST_STABLE",
        "history": history
    }
    
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    assert result["status"] == "normal"

def test_insufficient_data():
    input_data = {
        "history": [{"timestamp": "2026-01-01 00:00:00", "rms_value": 1.0}] * 10 # Only 10 points
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 1
    err = json.loads(stderr)
    assert "Insufficient data points" in err["message"]
