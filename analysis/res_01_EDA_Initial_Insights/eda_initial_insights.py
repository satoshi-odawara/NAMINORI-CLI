import pandas as pd
import numpy as np
import os

def eda_initial_insights():
    # 1. データの読み込み
    train = pd.read_csv('inputdata/train.csv')
    condition = pd.read_csv('inputdata/condition.csv')
    stadium = pd.read_csv('inputdata/stadium.csv')

    # 2. データの結合
    # train と condition を id で結合
    df = pd.merge(train, condition, on='id', how='left')
    # stadium を stadium名で結合 (trainではstadium, stadium.csvではname)
    df = pd.merge(df, stadium, left_on='stadium', right_on='name', how='left')

    # 3. 基本情報の確認
    output_path = 'analysis/res_01_EDA_Initial_Insights/eda_summary.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== DATA SHAPE ===\n")
        f.write(f"Train: {train.shape}\n")
        f.write(f"Condition: {condition.shape}\n")
        f.write(f"Stadium: {stadium.shape}\n")
        f.write(f"Merged: {df.shape}\n\n")

        f.write("=== NULL VALUES ===\n")
        f.write(df.isnull().sum().to_string())
        f.write("\n\n")

        f.write("=== Y (Attendance) SUMMARY ===\n")
        f.write(df['y'].describe().to_string())
        f.write("\n\n")

        # 物理境界チェック: capa を超えているデータがないか
        f.write("=== PHYSICAL BOUNDARY CHECK (y > capa) ===\n")
        invalid_y = df[df['y'] > df['capa']]
        f.write(f"Counts of y > capa: {len(invalid_y)}\n")
        if len(invalid_y) > 0:
            f.write(invalid_y[['id', 'y', 'capa', 'stadium']].to_string())
        f.write("\n\n")

        f.write("=== STAGE DISTRIBUTION ===\n")
        f.write(df['stage'].value_counts().to_string())
        f.write("\n")

    print(f"EDA Summary saved to {output_path}")

if __name__ == "__main__":
    eda_initial_insights()
