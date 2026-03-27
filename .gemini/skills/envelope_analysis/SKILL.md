# Skill: envelope_analysis

## 概要
ヒルベルト変換を用いて振動信号の包絡線（エンベロープ）を抽出し、そのスペクトルを分析します。ベアリングの局所欠陥（内輪、外輪、転動体）は高周波の共振を叩く周期的な衝撃を引き起こすため、エンベロープスペクトルに欠陥周波数が顕著に現れます。

## メタデータ
- カテゴリ: Classical
- バージョン: 1.0.0
- 担当ロール: Domain Expert
- 根拠手法: ヒルベルト変換, エンベロープスペクトル (HFRT)

## パラメータ
- `signal`: (Required) 振動データの数値配列。
- `fs`: (Required) サンプリング周波数 [Hz]。
- `equipment_id`: (Optional) 設備ID。
- `metadata.bearing_params`: (Optional) ベアリング諸元。
    - `fr`: 回転周波数 [Hz]。
    - `n`: 転動体数。
    - `d_D_ratio`: 転動体径/ピッチ円径 (d/D)。デフォルトは 0.2。

## ワークフロー
1. 振動データを読み込み、信号配列とサンプリング周波数を取得します。
2. ベアリング諸元（型番から計算または推定）を `bearing_params` に設定します。
3. `scripts/run_envelope.py` を実行します。
4. 出力JSONから、理論上の欠陥周波数（BPFO等）と実際のピークが一致するか確認します。
5. `assets/envelope_plot_{id}.png` をユーザーに提示し、ベアリングの異常部位を診断します。

## 入出力例
### 出力 (JSON 抜粋)
```json
{
  "status": "alert",
  "features": {
    "peak_frequencies": [105.0, 210.0, ...],
    "theory_bpfo": 105.0,
    "plot_url": ".../assets/envelope_plot_MOTOR_01.png"
  },
  "message": "Defect frequency detected at 105.00 Hz (Theory BPFO: 105.00 Hz)."
}
```
