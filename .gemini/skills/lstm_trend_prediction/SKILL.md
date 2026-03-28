# Skill: lstm_trend_prediction

## 概要
長短記憶 (LSTM) ネットワークを用いて、機械振動の時系列トレンドを将来予測します。従来の線形回帰では捉えられない、劣化の加速（指数関数的な増加）や複雑な変動パターンを学習し、ISO規格等の閾値に到達するまでの残存寿命 (RUL) を高精度に推定します。

## メタデータ
- カテゴリ: Deep Learning / Time-Series
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: LSTM (RNN)

## ワークフロー
1. 過去の複数回の計測結果（RMS等）を時系列データとして準備します（最小10点、推奨50点以上）。
2. `scripts/train_lstm.py` を実行して、対象機械の劣化傾向を学習させます。
3. 学習済みモデルを用い、`scripts/predict_lstm.py` で将来の推移を予測します。
4. 推定された RUL に基づき、メンテナンス時期を最適化します。

## パラメータ
- `equipment_id`: (Required) モデルのロードに使用します。
- `history`: (Required) 過去の計測値の配列。
- `threshold_value`: (Required) RUL算出の基準となる管理限界値。
- `metadata.horizon_days`: (Optional) 予測する将来の日数。デフォルト 30。

## 入出力例
### 出力 (抜粋)
```json
{
  "status": "warning",
  "features": {
    "remaining_useful_life_days": 14,
    "plot_url": ".gemini/skills/lstm_trend_prediction/assets/plots/PUMP_01_lstm_trend_20260328.png"
  },
  "message": "LSTM Prediction: WARNING. Estimated RUL: 14 days."
}
```
