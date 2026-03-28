# Skill: garch_volatility

## 概要
金融市場のボラティリティ推定に使われる GARCH(1,1) モデルを、設備の振動トレンド分析に応用します。振動値の絶対的な大きさ（RMS等）ではなく、その「ばらつきの変動」に着目します。ボラティリティの急増は、設備の物理的な不安定性（ガタ、支持剛性の低下、非定常な摩擦等）を示唆する早期警戒指標となります。

## メタデータ
- カテゴリ: Statistical
- バージョン: 1.0.0
- 担当ロール: Domain Expert
- 根拠手法: GARCH(1,1) (Generalized Autoregressive Conditional Heteroskedasticity)

## パラメータ
- `history`: (Required) 時系列データの配列（最小50点）。
    - `timestamp`: "YYYY-MM-DD HH:MM:SS"
    - `rms_value`: 解析対象の数値。
- `metadata.unit`: (Optional) 単位（例: "mms"）。

## ワークフロー
1. 長期（50日分以上推奨）のRMSトレンドデータを準備します。
2. `scripts/run_garch.py` を実行します。
3. 出力JSONの `conditional_volatility` とその履歴を確認します。
4. 平均ボラティリティに対して現在の値が 2倍を超えると `warning`、4倍を超えると `alert` と判定されます。
5. トレンドが一定でも、ボラティリティだけが先行して増大する場合、初期故障の兆候として詳細診断（FFT等）を推奨します。

## 入出力例
### 出力 (抜粋)
```json
{
  "status": "warning",
  "score": 2.5,
  "features": {
    "current_volatility": 0.45,
    "average_volatility": 0.18,
    "plot_url": ".gemini/skills/garch_volatility/assets/plots/MOTOR_01_garch_20260328.png"
  },
  "message": "Stability assessment: WARNING. Current instability factor is 2.50x of historical average."
}
```
