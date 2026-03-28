import subprocess
import json
import pytest
import os
import pandas as pd
import numpy as np

def run_script(script_name, stdin_dict=None, args=None):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", script_name)
    cmd = ["python", script_path]
    if args: cmd.extend(args)
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_dict else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdin_str = json.dumps(stdin_dict) if stdin_dict else None
    stdout, stderr = process.communicate(input=stdin_str)
    return process.returncode, stdout, stderr

def test_lstm_full_flow():
    # 1. Train on exponential fault data
    fault_csv = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "fault_exponential.csv")
    equipment_id = "QA_LSTM_FAN"
    
    rc_train, out_train, err_train = run_script("train_lstm.py", args=[fault_csv, equipment_id])
    assert rc_train == 0
    assert "success" in out_train

    # 2. Predict Future
    df = pd.read_csv(fault_csv)
    history = df.to_dict('records')
    # Exponential data ends around 6.5. Set threshold to 10.0
    input_data = {
        "equipment_id": equipment_id,
        "history": history,
        "threshold_value": 10.0,
        "metadata": {"horizon_days": 30}
    }
    
    rc_pred, out_pred, err_pred = run_script("predict_lstm.py", stdin_dict=input_data)
    assert rc_pred == 0
    res = json.loads(out_pred)
    
    # RUL should be detected as the trend is accelerating
    assert res["features"]["remaining_useful_life_days"] > 0
    assert res["status"] in ["warning", "alert"]
    
    # Check if plot was generated
    plot_path = os.path.join(os.path.dirname(__file__), "..", "assets", "plots")
    files = os.listdir(plot_path)
    assert any(f.startswith(equipment_id) for f in files)
