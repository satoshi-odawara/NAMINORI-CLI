import os
import joblib
import pandas as pd
import pytest

def test_model_assets_exist():
    # Check if model, importance, and feature names files are generated
    assert os.path.exists('analysis/res_03_Attendance_Prediction_Model/model.joblib')
    assert os.path.exists('analysis/res_03_Attendance_Prediction_Model/feature_importance.csv')
    assert os.path.exists('analysis/res_03_Attendance_Prediction_Model/feature_names.joblib')

def test_model_prediction():
    # Check if model can make predictions
    model = joblib.load('analysis/res_03_Attendance_Prediction_Model/model.joblib')
    feature_names = joblib.load('analysis/res_03_Attendance_Prediction_Model/feature_names.joblib')
    
    # Create a dummy sample with correct feature order
    sample_data = {f: [0] for f in feature_names}
    sample_df = pd.DataFrame(sample_data)[feature_names]
    
    prediction = model.predict(sample_df)
    assert len(prediction) == 1
    assert prediction[0] >= 0
