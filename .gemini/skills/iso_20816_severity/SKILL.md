# Skill: iso_20816_severity

## 概要
ISO 20816-3:2009 規格に基づき、振動速度の実効値 (RMS) から機械の状態（Zone A〜D）を自動判定します。設備容量や据付基礎の条件に応じた適切な評価を提供します。

## メタデータ
- カテゴリ: ISO-Standard
- バージョン: 1.0.0
- 担当ロール: All
- 根拠手法: ISO 20816-3:2009

## パラメータ
- `signal`: (Optional) 振動データの配列。指定された場合は RMS を計算します。
- `metadata.rms_value`: (Optional) 事前に計算された速度 RMS [mm/s]。`signal` がない場合に必須。
- `metadata.equipment_group`: (Required) 設備グループ (`group1`〜`group4`)。
    - `group1`: 大型機械 (> 300kW)
    - `group2`: 中型機械 (15kW - 300kW)
    - `group3`: 大型ポンプ
    - `group4`: 中型ポンプ
- `metadata.support_type`: (Required) 据付条件 (`rigid` | `flexible`)。

## ワークフロー
1. 振動データから RMS 値を算出（または `time_domain_features` スキルの出力を再利用）します。
2. 対象設備の容量と据付状態を確認し、`equipment_group` と `support_type` を設定します。
3. `scripts/iso_severity.py` を実行します。
4. 出力JSONの `zone` (A〜D) と `status` を確認し、メンテナンス判断の根拠とします。
5. `assets/plots/` に生成された重篤度プロットを報告書に添付します。

## 入出力例
### 入力
```json
{
  "equipment_id": "PUMP_001",
  "metadata": {
    "equipment_group": "group2",
    "support_type": "rigid",
    "rms_value": 3.2
  }
}
```

### 出力
```json
{
  "status": "warning",
  "features": {
    "zone": "C",
    "rms": 3.2,
    "plot_url": ".gemini/skills/iso_20816_severity/assets/plots/PUMP_001_iso_severity_20260328.png"
  },
  "message": "ISO Zone: C. RMS value: 3.20 mm/s. Support: rigid. Group: group2."
}
```
