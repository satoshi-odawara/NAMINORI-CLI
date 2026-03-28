import subprocess
import json
import pytest
import os
import pandas as pd
import numpy as np

def run_script(script_name, stdin_dict=None, args=None):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", script_name)
    cmd = ["python", script_path]
    if args:
        cmd.extend(args)
    
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

def test_full_autoencoder_flow():
    # 1. Train
    train_csv = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "train_normal.csv")
    equipment_id = "QA_TEST_DEVICE"
    
    rc_train, out_train, err_train = run_script("train.py", args=[train_csv, equipment_id])
    assert rc_train == 0
    res_train = json.loads(out_train)
    assert res_train["status"] == "success"
    threshold = res_train["threshold"]

    # 2. Infer Normal
    # Take first row from train_csv as features
    df_train = pd.read_csv(train_csv)
    normal_features = df_train.iloc[0].to_dict()
    
    input_normal = {
        "equipment_id": equipment_id,
        "metadata": {"features": normal_features}
    }
    rc_inf, out_inf, err_inf = run_script("infer.py", stdin_dict=input_normal)
    assert rc_inf == 0
    res_inf = json.loads(out_inf)
    assert res_inf["status"] == "normal"

    # 3. Infer Anomaly
    # Create a synthetic anomaly (Shifted features)
    anomaly_features = {k: v + 5.0 for k, v in normal_features.items()}
    input_anomaly = {
        "equipment_id": equipment_id,
        "metadata": {"features": anomaly_features}
    }
    rc_anom, out_anom, err_anom = run_script("infer.py", stdin_dict=input_anomaly)
    assert rc_anom == 0
    res_anom = json.loads(out_anom)
    assert res_anom["status"] == "alert"
    assert res_anom["features"]["reconstruction_error"] > threshold
