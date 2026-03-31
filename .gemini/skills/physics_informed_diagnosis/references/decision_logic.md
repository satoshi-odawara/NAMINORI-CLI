# Hybrid Decision Logic for ISSUE-0011

## 1. 物理安全層 (Physical Safety Layer)
ISO 20816-3 に基づく速度 RMS 判定を最優先する。
- **Zone D (Alert)**: 他の指標に関わらず、最終ステータスは `alert`。
- **Zone C (Warning)**: 最終ステータスは `warning` または `alert`（AI判定に依存）。
- **Zone A/B (Normal)**: 最終ステータスは `normal` または `warning`（AI判定に依存）。

## 2. 物理整合性 (Physics Consistency)
FFT のピーク周波数 $f_{peak}$ と、回転周波数 $f_r$ またはベアリング欠陥周波数（BPFO等）の整合性を確認する。
- 一致条件: $|f_{peak} - n \cdot f_r| < 0.05 \cdot f_r$ (n=1, 2, ...)
- 整合性が高い場合（一致する物理的故障モードがある場合）、診断結果の信頼度スコアを加算する。

## 3. AI 異常検知層 (AI Anomaly Detection Layer)
Autoencoder の異常スコア $S_{AE}$ を使用する。
- $S_{AE} > Threshold$: 「統計的にいつもと違う（Unknown Anomaly）」と判断。
- 物理層が Normal で AI が Alert の場合: **「正体不明の異常（要精密点検）」** として Warning を出す。

## 4. 信頼度スコアの算出式
$$Confidence = \alpha \cdot C_{physics} + \beta \cdot C_{AI}$$
ここで、
- $\alpha, \beta$: 重み付け係数（デフォルト 各0.5）
- $C_{physics}$: 物理的指標（ISO、FFT整合性）からの確信度
- $C_{AI}$: AIモデル（AE再構成誤差の小ささ、LSTM予測の分散）からの確信度

## 5. 最終判定マトリクス

| ISO Zone | AE Status | FFT Match | Final Status | Message |
|----------|-----------|-----------|--------------|---------|
| D | * | * | **Alert** | ISO規定による危険状態。即時停止。 |
| A/B/C | Alert | Yes | **Alert** | 特定の故障モード（FFT一致）を伴う異常。 |
| A/B/C | Alert | No | **Warning** | 原因不明の異常（AE検知）。精密診断推奨。 |
| A/B/C | Normal | Yes | **Warning** | 軽微な物理的兆候（FFT）。傾向監視。 |
| A/B | Normal | No | **Normal** | 設備状態は良好。 |

---
**引用**: ISO 20816-3:2022, "Mechanical vibration — Measurement and evaluation of machine vibration"
