import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# フォント設定 (日本語フォントがない環境を考慮)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

def save_plot(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches='tight', dpi=100)
    plt.close(fig)
    print(f"Saved: {path}")

def generate_eda_plots(df, output_dir):
    day_map = {0: '月', 1: '火', 2: '水', 3: '木', 4: '金', 5: '土', 6: '日'}
    
    # 1. J1/J2 比較
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='stage', y='y', data=df, ax=ax, palette='Set2', hue='stage', legend=False)
    ax.set_title('ディビジョン別観客動員数 (J1 vs J2)')
    save_plot(fig, os.path.join(output_dir, 'res_01_EDA_Initial_Insights/figures/y_by_stage.png'))

    # 2. 曜日別 × ディビジョン
    fig, ax = plt.subplots(figsize=(10, 6))
    df_plot = df.copy()
    df_plot['曜日'] = df_plot['day_of_week'].map(day_map)
    order = ['月', '火', '水', '木', '金', '土', '日']
    sns.barplot(x='曜日', y='y', hue='stage', data=df_plot, order=order, ax=ax, errorbar=None, palette='Set2')
    ax.set_title('ディビジョン・曜日別平均観客動員数')
    save_plot(fig, os.path.join(output_dir, 'res_01_EDA_Initial_Insights/figures/y_by_dow.png'))

    # 3. キャパ vs 動員
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x='capa', y='y', hue='stage', data=df, alpha=0.5, ax=ax, palette='Set2')
    ax.set_title('スタジアムキャパシティと動員数の相関')
    save_plot(fig, os.path.join(output_dir, 'res_01_EDA_Initial_Insights/figures/y_vs_capa.png'))

def generate_fe_plots(df, output_dir):
    # 4. 人気チームインパクト
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='stage', y='y', hue='is_popular', data=df, ax=ax, errorbar=None, palette='Set1')
    ax.set_title('人気チームフラグによる動員リフト (0:無, 1:有)')
    save_plot(fig, os.path.join(output_dir, 'res_02_Refined_Dataset/figures/popular_lift.png'))

    # 5. ダービーインパクト (J1のみサンプルがあるためフィルタリングを考慮)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='stage', y='y', hue='is_derby', data=df[df['stage']=='Ｊ１'], ax=ax, errorbar=None, palette='Set1')
    ax.set_title('ダービーフラグによる動員リフト (J1限定, 0:無, 1:有)')
    save_plot(fig, os.path.join(output_dir, 'res_02_Refined_Dataset/figures/derby_lift.png'))

def generate_model_plots(importance_path, output_dir):
    # 6. 特徴量重要度
    if os.path.exists(importance_path):
        imp_df = pd.read_csv(importance_path)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=imp_df.sort_values('importance', ascending=False), ax=ax, palette='magma', hue='feature', legend=False)
        ax.set_title('観客動員予測における重要要因 (Random Forest)')
        save_plot(fig, os.path.join(output_dir, 'res_03_Attendance_Prediction_Model/figures/feature_importance.png'))

if __name__ == "__main__":
    root = "analysis"
    train_path = os.path.join(root, "res_02_Refined_Dataset/merged_train.csv")
    if os.path.exists(train_path):
        df = pd.read_csv(train_path)
        generate_eda_plots(df, root)
        generate_fe_plots(df, root)
    
    importance_path = os.path.join(root, "res_03_Attendance_Prediction_Model/feature_importance.csv")
    generate_model_plots(importance_path, root)
