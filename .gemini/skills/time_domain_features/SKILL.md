# Skill: time_domain_features

## 概要
振動波形から、RMS（実効値）、尖度、波高率（クレストファクタ）等の時間領域統計的特徴量を一括抽出します。これらの指標は、全体の振動レベルの把握や、ベアリング等の衝撃的な異常の初期検知に有効です。

## メタデータ
- カテゴリ: Classical
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: 統計解析（RMS, Kurtosis, Crest Factor, Skewness）

## 指標の説明
- `rms`: 振動エネルギーの総量。ISO 20816-3の評価対象。
- `kurtosis`: 尖度。Fisherの定義（超過尖度）を採用しており、正規分布では 0 です。**3.0を超えると衝撃成分の存在（ベアリング損傷等）が強く疑われます。**
- `crest_factor`: 波高率。ピーク値とRMSの比。軸受の状態監視に用いられます。
- `skewness`: 歪度。波形の非対称性を示します。

## パラメータ
- `signal`: (Required) 振動データの数値配列。
- `fs`: (Required) サンプリング周波数 [Hz]。
- `equipment_id`: (Optional) 設備ID。

## ワークフロー
1. 振動データ（CSV等）から信号配列を取得します。
2. `scripts/extract_time_features.py` を実行し、統計量を抽出します。
3. 出力JSONから `rms` と `kurtosis` を中心に状態を判断します。
4. 生成された時間波形プロット（`assets/time_plot_{id}.png`）を確認し、パルス状のノイズがないか視認します。

## 入出力例
### 出力 (JSON 抜粋)
```json
{
  "status": "warning",
  "score": 1.25,
  "features": {
    "rms": 1.25,
    "kurtosis": 5.2,
    "crest_factor": 4.5,
    "plot_url": ".../assets/time_plot_PUMP_01.png"
  },
  "message": "High Kurtosis detected (possible impact noise/bearing fault)."
}
```
