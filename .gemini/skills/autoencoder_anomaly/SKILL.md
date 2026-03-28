# Skill: autoencoder_anomaly

## 概要
正常状態の多次元特徴量のみを学習したニューラルネットワーク（オートエンコーダ）を用い、未知の入力信号に対する「正常からの逸脱度」を検知します。特定の故障モードを定義することなく、総合的な「いつもと違う」状態をスコア化できるため、教師なし学習による高度な異常検知が可能です。

## メタデータ
- カテゴリ: Deep Learning
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: オートエンコーダ（再構成誤差）

## ワークフロー
このスキルは「訓練」と「推論」の2段階で使用します。

### 1. 訓練 (Training)
正常運転時の特徴量（MFCC, RMS, 統計量等）をCSV形式で準備し、以下のコマンドでモデルを作成します。
```powershell
python scripts/train.py path/to/normal_data.csv {equipment_id}
```
これにより `assets/models/` にモデルと閾値設定が保存されます。

### 2. 推論 (Inference)
他のスキル（`mfcc_features`等）の出力を入力として、現在の異常スコアを算出します。
§6.8 のパイプラインルールに基づき、`metadata.features` に特徴量辞書を渡してください。

## パラメータ
- `equipment_id`: (Required) モデルのロードに使用します。
- `metadata.features`: (Required) 多次元特徴量の辞書（MFCC, rms, kurtosis 等を含む）。

## 入出力例
### 入力
```json
{
  "equipment_id": "MOTOR_01",
  "metadata": {
    "features": {
      "mfcc_0": -250.1,
      "rms": 1.5,
      "kurtosis": 0.1
    }
  }
}
```

### 出力 (抜粋)
```json
{
  "status": "normal",
  "score": 0.45,
  "features": {
    "reconstruction_error": 0.012,
    "threshold": 0.025
  },
  "message": "Anomaly detection: NORMAL. Error: 0.0120 (Threshold: 0.0250)"
}
```
