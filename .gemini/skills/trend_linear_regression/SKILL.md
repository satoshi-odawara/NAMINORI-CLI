# Skill: trend_linear_regression

## 概要
蓄積された時系列データに対して線形回帰を行い、将来の振動レベルを予測します。設定された閾値（ISO規格値等）に到達するまでの推定日数（RUL: Remaining Useful Life）を算出し、予防保全の計画立案を支援します。

## メタデータ
- カテゴリ: Statistical
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: 最小二乗法 (Linear Regression)

## パラメータ
- `history`: (Required) 日時と計測値の配列。
    - `timestamp`: "YYYY-MM-DD HH:MM:SS" 形式。
    - `rms_value`: 計測された数値。
- `threshold_value`: (Required) 到達予測の対象とする閾値。
- `equipment_id`: (Optional) 設備ID。

## ワークフロー
1. 過去の複数回の診断結果（RMS値など）を `history` としてまとめます。
2. 目標とする管理限界値を `threshold_value` に設定します。
3. `scripts/predict_trend.py` を実行します。
4. 出力JSONの `remaining_useful_life_days` を確認し、30日を切る場合は `warning`、7日を切る場合は `alert` として評価します。
5. `r_squared` (決定係数) を確認し、0.7 未満の場合は予測の信頼性が低い（ばらつきが大きい）と判断します。

## 入出力例
### 入力
```json
{
  "history": [
    {"timestamp": "2026-03-01 09:00:00", "rms_value": 1.2},
    {"timestamp": "2026-03-15 09:00:00", "rms_value": 2.5}
  ],
  "threshold_value": 7.1,
  "equipment_id": "FAN_01"
}
```

### 出力 (抜粋)
```json
{
  "status": "normal",
  "features": {
    "predicted_threshold_date": "2026-05-20",
    "remaining_useful_life_days": 53,
    "r_squared": 0.98,
    "plot_url": ".gemini/skills/trend_linear_regression/assets/plots/FAN_01_trend_20260328.png"
  }
}
```
