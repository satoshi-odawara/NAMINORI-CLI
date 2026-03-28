import subprocess
import json
import pytest
import os
import numpy as np
import pandas as pd

def run_script(input_dict):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "run_mfcc.py")
    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_dict))
    return process.returncode, stdout, stderr

def test_mfcc_extraction():
    csv_normal = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "normal_hum.csv")
    df = pd.read_csv(csv_normal)
    
    input_data = {
        "equipment_id": "TEST_NORMAL",
        "signal": df['amplitude'].tolist(),
        "fs": 22050
    }
    
    rc, stdout, stderr = run_script(input_data)
    if rc != 0:
        print(stderr)
    assert rc == 0
    result = json.loads(stdout)
    assert "mfcc_mean" in result["features"]
    assert len(result["features"]["mfcc_mean"]) == 13

def test_mfcc_difference():
    # Compare normal vs squeal
    csv_normal = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "normal_hum.csv")
    csv_fault = os.path.join(os.path.dirname(__file__), "..", "assets", "synthetic", "fault_squeal.csv")
    
    df_n = pd.read_csv(csv_normal)
    df_f = pd.read_csv(csv_fault)
    
    res_n = json.loads(run_script({"signal": df_n['amplitude'].tolist(), "fs": 22050})[1])
    res_f = json.loads(run_script({"signal": df_f['amplitude'].tolist(), "fs": 22050})[1])
    
    mfcc_n = np.array(res_n["features"]["mfcc_mean"])
    mfcc_f = np.array(res_f["features"]["mfcc_mean"])
    
    # Euclidean distance between feature vectors should be significant
    dist = np.linalg.norm(mfcc_n - mfcc_f)
    assert dist > 10.0 # Significant difference in spectral envelope
