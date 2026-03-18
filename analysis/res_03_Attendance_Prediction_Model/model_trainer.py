import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

def train_and_analyze():
    # Load data
    df = pd.read_csv('analysis/res_02_Refined_Dataset/merged_train.csv')
    
    # Selection of Features (Pre-match info only)
    features = [
        'stage', 'month', 'day_of_week', 'weather_cat', 
        'is_popular', 'is_derby', 'capa'
    ]
    
    # Target variable y (attendance)
    y = df['y']
    X = df[features].copy()
    
    # Preprocessing: Encoding categorical variables
    X = pd.get_dummies(X, columns=['stage', 'weather_cat'], drop_first=True)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training: RandomForestRegressor for cause analysis (feature importance)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Model RMSE: {rmse:.2f}")
    
    # Feature Importance (Cause Analysis)
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Save Model, Analysis Results, and Feature Names
    output_dir = 'analysis/res_03_Attendance_Prediction_Model/'
    model_path = os.path.join(output_dir, 'model.joblib')
    importance_path = os.path.join(output_dir, 'feature_importance.csv')
    features_path = os.path.join(output_dir, 'feature_names.joblib')
    
    joblib.dump(model, model_path)
    importance.to_csv(importance_path, index=False, encoding='utf-8')
    joblib.dump(X.columns.tolist(), features_path)
    
    # Print Top Important Features
    print("\nTop Features Contributing to Attendance:")
    print(importance.head(10))
    
    # Physical Validity Check (Manager Role)
    print("\n[QA/Physical Validity Check]")
    # Urawa Reds penalty (y=0) check
    penalty_matches = df[df['y'] == 0]
    if not penalty_matches.empty:
        print(f"Warning: {len(penalty_matches)} penalty matches (y=0) detected. Training included these as outliers.")
    
    return model, rmse, importance

if __name__ == "__main__":
    train_and_analyze()
