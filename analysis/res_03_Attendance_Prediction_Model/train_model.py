import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

def train_and_evaluate():
    # 1. データの読み込み
    df = pd.read_csv('analysis/res_02_Refined_Dataset/train_preprocessed.csv')

    # 2. 学習用とテスト用に分割
    # 目的変数 y, 特徴量 X
    X = df.drop(['id', 'y'], axis=1)
    y = df['y']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. モデルの構築 (RandomForest)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. 予測と評価
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # 5. 特徴量重要度の算出
    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    # 6. 結果の保存
    output_path = 'analysis/res_03_Attendance_Prediction_Model/model_summary.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== MODEL EVALUATION ===\n")
        f.write(f"Algorithm: RandomForestRegressor\n")
        f.write(f"RMSE: {rmse:.2f}\n\n")

        f.write("=== FEATURE IMPORTANCE ===\n")
        f.write(importances.to_string(index=False))
        f.write("\n")

    print(f"Model evaluation saved to {output_path}")

if __name__ == "__main__":
    train_and_evaluate()
