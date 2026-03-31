# Physics-Informed Integrated Diagnosis (ISSUE-0011)

## 概要
このスキルは、個別解析スキル（FFT, ISO, AE, LSTM等）の出力を統合し、物理則とAIモデルの両面から最終的な設備診断を行う「ハイブリッド型PdM診断エンジン」です。単なる多数決ではなく、ISO規格（物理安全）と異常検知（AI）の矛盾を解消し、信頼性の高い最終提言を生成します。

## ワークフロー (Agent Pipeline)
1. **データ収集**: `time_domain_features`, `fft_spectrum`, `autoencoder_anomaly`, `lstm_trend_prediction` の出力 JSON を読み込む。
2. **物理検証 (Physics Check)**: 
    - ISO 20816-3 の閾値との照合。
    - FFTピークが回転速度(1X, 2X)やベアリング故障周波数(BPFO/BPFI)と一致するか検証。
3. **AI検証 (Data-Driven Check)**: 
    - Autoencoder による異常スコアの評価。
    - LSTM による将来的な閾値到達までの RUL 推定。
4. **統合判断 (Synthesis)**: 
    - 物理（ISO/FFT）と AI（AE/LSTM）の判定を統合し、最終ステータスと信頼度スコアを算出。
    - 矛盾（例：ISO正常だがAEがAlert）がある場合、その理由（「正体不明の不連続振動」等）を言語化。

## 推奨パラメータ (Input Schema)
```json
{
  "inputs": {
    "iso_20816": { "status": "...", "rms_value": 0.0, "zone": "..." },
    "fft_spectrum": { "dominant_frequency": 0.0, "peak_frequencies": [] },
    "autoencoder": { "anomaly_score": 0.0, "status": "..." },
    "lstm_trend": { "remaining_useful_life_days": 0 }
  },
  "metadata": {
    "equipment_id": "...",
    "bearing_params": { "fr": 0.0, "n": 0, "d_D_ratio": 0.0 }
  }
}
```

## 出力 (Output Schema)
```json
{
  "status": "normal|warning|alert|error",
  "score": 0.0,  // 信頼度スコア (0.0-1.0)
  "method": "physics_informed_diagnosis",
  "features": {
    "overall_status": "...",
    "confidence_score": 0.0,
    "conflicting_indicators": [],
    "recommended_action": "...",
    "next_inspection_date": "YYYY-MM-DD",
    "plot_url": "assets/plots/{equipment_id}_integrated_{timestamp}.png"
  },
  "message": "物理とAIの統合診断結果の説明（日本語）"
}
```

## 依存関係
- ISSUE-0001, ISSUE-0003, ISSUE-0004, ISSUE-0009, ISSUE-0010
- Python 3.8+ (numpy, scipy, pandas, matplotlib)
