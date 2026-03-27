import subprocess
import json
import pytest
import os
import pandas as pd

def run_script(input_dict):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "predict_trend.py")
    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_dict))
    return process.returncode, stdout, stderr

def test_linear_trend_prediction():
    # Load fault trend data (Increasing from 1.0 to 6.0 over 30 days)
    csv_path = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "fault_trend.csv")
    df = pd.read_csv(csv_path)
    history = df.to_dict('records')
    
    # Set threshold to 7.1 (ISO Group 1 Rigid boundary)
    input_data = {
        "equipment_id": "TEST_FAULT_TREND",
        "history": history,
        "threshold_value": 7.1
    }
    
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    
    assert result["features"]["slope"] > 0
    assert result["features"]["r_squared"] > 0.9
    assert result["features"]["remaining_useful_life_days"] > 0
    assert result["status"] in ["normal", "warning", "alert"]

def test_stable_trend():
    # Stable data (Slope ~ 0)
    history = [
        {"timestamp": "2026-03-01 00:00:00", "rms_value": 1.0},
        {"timestamp": "2026-03-02 00:00:00", "rms_value": 1.0},
        {"timestamp": "2026-03-03 00:00:00", "rms_value": 0.9}
    ]
    input_data = {
        "equipment_id": "TEST_STABLE",
        "history": history,
        "threshold_value": 5.0
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    assert "No threshold hit predicted" in result["message"]
    assert result["features"]["remaining_useful_life_days"] == -1

def test_insufficient_data():
    input_data = {
        "history": [{"timestamp": "2026-03-01 00:00:00", "rms_value": 1.0}], # Only 1 point
        "threshold_value": 5.0
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 1
    err = json.loads(stderr)
    assert err["error_code"] == "COMPUTATION_FAILED"
