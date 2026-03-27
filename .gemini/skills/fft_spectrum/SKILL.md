# Skill: fft_spectrum

## 概要
時系列振動データを周波数領域に変換し、パワースペクトル密度（PSD）を算出します。回転機械の各故障モード（不釣り合い、ミスアライメント、ベアリング欠陥等）に特有の周波数成分を特定するための基礎的な解析手法です。

## メタデータ
- カテゴリ: Classical
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: FFT（高速フーリエ変換）

## パラメータ
- `signal`: (Required) 振動データの数値配列。
- `fs`: (Required) サンプリング周波数 [Hz]。
- `equipment_id`: (Optional) 設備ID。プロットのファイル名に使用されます。
- `metadata.window`: (Optional) 使用する窓関数。デフォルトは `hann`。他に `hamming`, `flattop`, `boxcar` 等が指定可能。

## ワークフロー
1. 振動データ（CSV等）を読み込み、信号配列とサンプリング周波数を取得します。
2. `scripts/run_fft.py` を実行し、JSON入力を標準入力から渡します。
3. 出力JSONから `dominant_frequency` と `psd` を解析します。
4. `assets/` に生成されたプロット画像（`fft_plot_{id}.png`）をユーザーに提示し、診断結果の証拠とします。

## 入出力例
### 入力 (JSON)
```json
{
  "signal": [0.1, -0.2, 0.3, ...],
  "fs": 1000,
  "equipment_id": "PUMP_001",
  "metadata": { "window": "hann" }
}
```

### 出力 (JSON)
```json
{
  "status": "normal",
  "score": 0.123,
  "method": "fft_spectrum",
  "features": {
    "frequencies": [0, 1, 2, ...],
    "psd": [0.001, 0.005, ...],
    "dominant_frequency": 10.0,
    "plot_url": ".../assets/fft_plot_PUMP_001.png"
  },
  "message": "Dominant frequency detected at 10.00 Hz."
}
```
