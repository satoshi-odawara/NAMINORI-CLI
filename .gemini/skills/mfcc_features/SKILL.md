# Skill: mfcc_features

## 概要
メル周波数ケプストラム係数 (MFCC) を抽出します。MFCC は音声認識で広く使われる特徴量で、信号のスペクトル包絡（音色）を効果的に圧縮・表現します。PdMにおいては、異なる故障モード（不釣り合い、ミスアライメント、異音を伴うベアリング欠陥等）の「シグネチャー」を捉えるための強力な高次元特徴量として機能します。

## メタデータ
- カテゴリ: Classical / Signal Processing
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: メル尺度フィルタバンク、離散コサイン変換 (DCT)

## パラメータ
- `signal`: (Required) 振動データの数値配列。
- `fs`: (Required) サンプリング周波数 [Hz]。
- `equipment_id`: (Optional) 設備ID。
- `metadata.n_mfcc`: (Optional) 抽出する係数の数。デフォルト 13。
- `metadata.n_fft`: (Optional) FFT 窓長。
- `metadata.hop_length`: (Optional) フレーム間隔。

## ワークフロー
1. 振動波形データを取得します。
2. `scripts/run_mfcc.py` を実行します。
3. 出力JSONの `mfcc_mean` を確認します。これは各係数の時間平均であり、その時点での設備の「音の特徴」を13次元程度のベクトルで表したものです。
4. この出力は、後続の `autoencoder_anomaly` スキルの訓練データおよび推論入力としてそのまま使用することを推奨します。

## 入出力例
### 入力
```json
{
  "signal": [...],
  "fs": 22050,
  "equipment_id": "PUMP_01",
  "metadata": { "n_mfcc": 13 }
}
```

### 出力 (抜粋)
```json
{
  "status": "normal",
  "features": {
    "mfcc_mean": [-200.5, 120.3, -15.2, ...],
    "n_mfcc": 13,
    "plot_url": ".gemini/skills/mfcc_features/assets/plots/PUMP_01_mfcc_20260328.png"
  },
  "message": "Extracted 13 MFCC features."
}
```
