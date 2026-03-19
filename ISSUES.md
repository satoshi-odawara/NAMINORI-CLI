# ISSUES.md

## 進行中のイシュー
- なし

## 完了したイシュー
- [x] [ISSUE-01] データ理解・探索的データ分析 (EDA)
- [x] [ISSUE-02] 特徴量エンジニアリング & 前処理
- [x] [ISSUE-03] モデル構築・評価
- [x] [ISSUE-04] 分析結果の統合と最終報告

---

## イシュー詳細

### [ISSUE-01] データ理解・探索的データ分析 (EDA) [CLOSED]
- [x] データの読み込みと基本情報の確認 (dtypes, non-null counts)
- [x] 目的変数 `y` の分布確認
- [x] カテゴリカル変数（スタジアム、天候、節）と `y` の関係の可視化
- [x] スタジアムキャパシティ (`capa`) と `y` の関係の確認
- [x] 成果物の集約管理化 (`analysis/res_01_EDA_Initial_Insights/`)

### [ISSUE-02] 特徴量エンジニアリング & 前処理 [CLOSED]
- [x] `train.csv`, `condition.csv`, `stadium.csv` の外部キー結合
- [x] 日付・時刻データのパース（曜日、ナイトゲーム/デイゲーム等）
- [x] 欠損値の適切な処理 (referee fillna)
- [x] 人気チームフラグ、ダービーマッチフラグの作成
- [x] 天候の簡略カテゴリ化 (weather_cat)
- [x] ドメイン知識の定数化 (`constants.py`)
- [x] 成果物の集約管理化 (`analysis/res_02_Refined_Dataset/`)

### [ISSUE-03] モデル構築・評価 [CLOSED]
- [x] ベースラインモデル (RandomForestRegressor) の作成
- [x] 特徴量重要度による要因分析 (Feature Importance)
- [x] 予測精度評価 (RMSE: 3549)
- [x] 推論用特徴量順序の固定化 (`feature_names.joblib`)
- [x] 成果物の集約管理化 (`analysis/res_03_Attendance_Prediction_Model/`)

### [ISSUE-04] 分析結果の統合と最終報告 [CLOSED]
- [x] 各フェーズのレポート統合
- [x] 現場向け集客改善アクションの具体化
- [x] 最終納品資産の整理

