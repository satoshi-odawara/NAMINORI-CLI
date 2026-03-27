# Skill: iso_10816_compatibility

## 概要
振動速度信号 [mm/s] を積分して変位 [µm] を算出し、旧規格 ISO 10816 に基づく評価（Zone A〜D）を行います。速度評価が主流となった現在でも、変位評価を必要とするレガシー設備や特定の保守基準に対応するために使用されます。

## メタデータ
- カテゴリ: ISO-Standard
- バージョン: 1.0.0
- 担当ロール: Domain Expert
- 根拠手法: ISO 10816 (積分による変位ピーク評価)

## パラメータ
- `signal`: (Required) 振動速度の数値配列 [mm/s]。
- `fs`: (Required) サンプリング周波数 [Hz]。
- `equipment_id`: (Optional) 設備ID。

## ワークフロー
1. 振動速度データを取得します。
2. `scripts/run_iso_10816.py` を実行します。
3. 積分によるドリフトを防ぐため、内部で自動的に 10Hz のハイパスフィルタが適用されます。
4. 出力JSONから `displacement_p2p_um` (ピーク-ピーク変位) と `iso_10816_zone` を確認します。
5. `assets/plots/` に保存された速度波形と変位波形の対比プロットを確認します。

## 入出力例
### 入力 (JSON)
```json
{
  "signal": [0.5, 1.2, -0.3, ...],
  "fs": 5000,
  "equipment_id": "LEGACY_MOTOR_01"
}
```

### 出力 (JSON)
```json
{
  "status": "normal",
  "features": {
    "velocity_rms_mms": 7.07,
    "displacement_p2p_um": 31.8,
    "iso_10816_zone": "B",
    "plot_url": ".gemini/skills/iso_10816_compatibility/assets/plots/LEGACY_MOTOR_01_iso10816_20260328.png"
  },
  "message": "ISO 10816 Zone B. Displacement P-P: 31.8 µm. Velocity RMS: 7.07 mm/s."
}
```
