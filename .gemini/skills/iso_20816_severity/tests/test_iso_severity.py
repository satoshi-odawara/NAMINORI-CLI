import subprocess
import json
import pytest
import os

def run_script(input_dict):
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "iso_severity.py")
    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_dict))
    return process.returncode, stdout, stderr

def test_zone_a():
    # Group 2, Rigid: Zone A <= 1.4
    input_data = {
        "equipment_id": "TEST_A",
        "metadata": {"equipment_group": "group2", "support_type": "rigid", "rms_value": 1.0}
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    assert result["features"]["zone"] == "A"
    assert result["status"] == "normal"

def test_zone_c_warning():
    # Group 1, Rigid: 4.5 < Zone C <= 7.1
    input_data = {
        "equipment_id": "TEST_C",
        "metadata": {"equipment_group": "group1", "support_type": "rigid", "rms_value": 5.0}
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    assert result["features"]["zone"] == "C"
    assert result["status"] == "warning"

def test_zone_d_alert():
    # Group 4, Flexible: Zone D > 7.1
    input_data = {
        "equipment_id": "TEST_D",
        "metadata": {"equipment_group": "group4", "support_type": "flexible", "rms_value": 15.0}
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 0
    result = json.loads(stdout)
    assert result["features"]["zone"] == "D"
    assert result["status"] == "alert"

def test_invalid_param_error():
    input_data = {
        "equipment_id": "TEST_ERR",
        "metadata": {"equipment_group": "invalid", "support_type": "rigid", "rms_value": 1.0}
    }
    rc, stdout, stderr = run_script(input_data)
    assert rc == 1
    error_res = json.loads(stderr)
    assert error_res["status"] == "error"
    assert "equipment_group" in error_res["message"]
