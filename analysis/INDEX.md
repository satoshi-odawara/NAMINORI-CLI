# Jリーグ観客動員数予測分析：分析ポータル

本ディレクトリには、Jリーグ観客動員数予測に関する全ての分析成果物と運用記録が格納されています。
初めての方は、まず「**0. 最終報告書**」からご覧ください。

---

## 📊 分析レポート一覧

各レポートは、Markdown（開発用）と HTML（閲覧・印刷用）の2形式で提供されています。

### 0. 最終報告書 (Final Report)
分析の総括と、現場で取るべきアクションプランをまとめています。
- [**HTML版で読む（推奨）**](res_04_Final_Report/FINAL_REPORT_Attendance_Prediction.html)
- [Markdown版](res_04_Final_Report/FINAL_REPORT_Attendance_Prediction.md)

### 1. 探索的データ分析 (EDA)
データの分布、J1/J2の構造的な動員格差、無観客試合の特定など、初期の洞察をまとめています。
- [HTML版](res_01_EDA_Initial_Insights/REPORT_EDA.html)
- [Markdown版](res_01_EDA_Initial_Insights/REPORT_EDA.md)

### 2. 特徴量エンジニアリング & 前処理
天候の集約、人気チーム・ダービーフラグなど、ドメイン知識を変数化した過程をまとめています。
- [HTML版](res_02_Refined_Dataset/REPORT_Feature_Engineering.html)
- [Markdown版](res_02_Refined_Dataset/REPORT_Feature_Engineering.md)

### 3. モデル構築 & 要因分析
Random Forestを用いた予測モデル（RMSE: 3549）と、動員を決定付ける主要因の定量化結果です。
- [HTML版](res_03_Attendance_Prediction_Model/REPORT_Modeling.html)
- [Markdown版](res_03_Attendance_Prediction_Model/REPORT_Modeling.md)

---

## 🛠️ 管理・運用ドキュメント（プロセスの透明性）
分析の背景、物理的制約、意思決定の履歴を公開しています。

- [**分析計画書 & ジャーナル (HTML版)**](analysis_plan.html) / [Markdown版](analysis_plan.md)
- [**案件固有ルール (HTML版)**](PROJECT_SPECIFIC_RULES.html) / [Markdown版](PROJECT_SPECIFIC_RULES.md)
- [**品質改善ログ (HTML版)**](REVIEW_LOG.html) / [Markdown版](REVIEW_LOG.md)

---
&copy; 2026 NAMINORI Data Science Team.
