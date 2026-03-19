import pandas as pd
import numpy as np
import os
import sys

# constants.py を読み込むためパスを追加
sys.path.append('analysis')
from constants import POPULAR_TEAMS, WEATHER_MAP, WEEK_MAP

def preprocess():
    # 1. データの読み込み
    train = pd.read_csv('inputdata/train.csv')
    condition = pd.read_csv('inputdata/condition.csv')
    stadium = pd.read_csv('inputdata/stadium.csv')

    # 2. データの結合
    df = pd.merge(train, condition, on='id', how='left')
    df = pd.merge(df, stadium, left_on='stadium', right_on='name', how='left')

    # 3. 特徴量エンジニアリング
    
    # 月と曜日の抽出 (gameday: MM/DD(曜日))
    df['month'] = df['gameday'].apply(lambda x: int(x[:2]))
    df['week'] = df['gameday'].apply(lambda x: x[6:7])
    df['week_num'] = df['week'].map(WEEK_MAP)
    
    # 土日祝フラグ (簡易的に土日を 1 とする)
    df['is_holiday'] = df['week'].apply(lambda x: 1 if x in ['土', '日', '祝'] else 0)

    # 天候の簡略化
    # 複数の天候が記載されている場合は、先頭の天候を優先する
    def simplify_weather(w):
        for k, v in WEATHER_MAP.items():
            if k in w:
                return v
        return 'Other'
    df['weather_cat'] = df['weather'].apply(simplify_weather)

    # 人気チームフラグ
    df['is_popular_home'] = df['home'].apply(lambda x: 1 if x in POPULAR_TEAMS else 0)
    df['is_popular_away'] = df['away'].apply(lambda x: 1 if x in POPULAR_TEAMS else 0)

    # 4. モデル用データの作成
    # 今回はベースラインとして数値化・カテゴリ化された特徴量を選択
    features = [
        'id', 'y', 'year', 'stage', 'month', 'week_num', 'is_holiday',
        'weather_cat', 'is_popular_home', 'is_popular_away', 'capa'
    ]
    df_refined = df[features].copy()

    # カテゴリ変数のダミー化
    df_refined = pd.get_dummies(df_refined, columns=['stage', 'weather_cat'])

    # 5. 保存
    output_path = 'analysis/res_02_Refined_Dataset/train_preprocessed.csv'
    df_refined.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess()
