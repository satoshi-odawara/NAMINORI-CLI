# データ分析スクリプト実装規約（実装・運用ガイドライン）

本ドキュメントは、`gemini.md` 技術憲章に基づき、具体的なコーディング、解析アルゴリズム、およびツールの運用ルールを定義する。

---

## 1. 技術スタック

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Data Processing:** NumPy, SciPy (signal, fft)
* **Visualization:** Plotly

---

## 2. 共通コーディング規約

### 2.1 物理量・単位の明示

* すべての数値は **物理量 + 単位** を前提とする。
* 変数名には必ず単位を含める。
  * 例：`accel_ms2`, `vel_mms`, `disp_um`, `freq_hz`, `time_s`

### 2.2 物理量種別の明示（必須）

加速度・速度・変位を混在させないため、解析関数には必ず物理量種別を明示する。

```python
from enum import Enum

class SignalQuantity(Enum):
    ACCEL = "accel"        # m/s^2
    VELOCITY = "velocity" # mm/s
    DISPLACEMENT = "disp" # μm
```

---

## 3. 運用・保守ガイドライン

### 3.1 `replace` ツール使用規約

* **厳密な一致:** `old_string` は改行・空白含めターゲットと完全に一致させること。
* **大規模変更:** リファクタリング時は `read_file` -> `write_file` 方式を推奨。
