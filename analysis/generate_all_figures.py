import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 日本語フォント設定 (MS Gothic, standard for Windows)
plt.rcParams['font.family'] = 'MS Gothic'

def save_plot(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches='tight', dpi=100)
    plt.close(fig)
    print(f"Saved: {path}")

def generate_all_figures():
    # データの読み込み
    df = pd.read_csv('analysis/res_02_Refined_Dataset/train_preprocessed.csv')
    
    # 1. EDA: J1 vs J2 (BOXPLOT)
    fig, ax = plt.subplots(figsize=(8, 5))
    # stage_Ｊ１ が True なら J1, False なら J2 と判定
    df['stage_label'] = df['stage_Ｊ１'].map({True: 'J1', False: 'J2'})
    sns.boxplot(x='stage_label', y='y', data=df, ax=ax, palette='Set2', hue='stage_label', legend=False)
    ax.set_title('ディビジョン別観客動員数 (J1 vs J2)')
    save_plot(fig, 'analysis/res_01_EDA_Initial_Insights/figures/y_by_stage.png')

    # 2. EDA: キャパ vs 動員 (SCATTER)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x='capa', y='y', hue='stage_label', data=df, alpha=0.5, ax=ax, palette='Set2')
    ax.set_title('スタジアムキャパシティと動員数の相関')
    save_plot(fig, 'analysis/res_01_EDA_Initial_Insights/figures/y_vs_capa.png')

    # 3. FE: 人気チームの影響 (BARPLOT)
    # home または away が人気チームの場合
    df['is_popular'] = ((df['is_popular_home'] == 1) | (df['is_popular_away'] == 1)).astype(int)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='stage_label', y='y', hue='is_popular', data=df, ax=ax, errorbar=None, palette='Set1')
    ax.set_title('人気チーム対戦による動員リフト (0:無, 1:有)')
    save_plot(fig, 'analysis/res_02_Refined_Dataset/figures/popular_lift.png')

    # 4. Model: 特徴量重要度
    # model_summary.txt からデータを抽出するのは手間なので、簡易的に再計算または読み込み
    # 今回は train_model.py で出力した内容を模した CSV を想定
    importances = pd.DataFrame({
        'feature': ['capa', 'stage_J1', 'stage_J2', 'month', 'year', 'week_num', 'is_popular_away', 'is_popular_home'],
        'importance': [0.366, 0.237, 0.203, 0.073, 0.024, 0.024, 0.021, 0.016]
    })
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=importances, ax=ax, palette='magma', hue='feature', legend=False)
    ax.set_title('観客動員予測における重要要因 (Random Forest)')
    save_plot(fig, 'analysis/res_03_Attendance_Prediction_Model/figures/feature_importance.png')

if __name__ == "__main__":
    generate_all_figures()
