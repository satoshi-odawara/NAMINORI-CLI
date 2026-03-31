import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def calculate_confidence(iso_zone, ae_status, fft_match):
    """
    信頼度スコアを算出する (0.0 - 1.0)
    """
    score = 0.5  # ベースライン
    
    # 物理とAIの整合性チェック
    if iso_zone in ['C', 'D'] and ae_status == 'alert':
        score += 0.3  # 両方異常なら確信度アップ
    elif iso_zone in ['A', 'B'] and ae_status == 'normal':
        score += 0.3  # 両方正常なら確信度アップ
    else:
        score -= 0.2  # 矛盾がある場合は確信度ダウン
        
    # FFT整合性による補正
    if fft_match:
        score += 0.2
        
    return min(max(score, 0.1), 1.0)

def get_integrated_status(iso_zone, ae_status, fft_match):
    """
    統合ステータスを決定する
    """
    if iso_zone == 'D':
        return 'alert', "ISO規定による危険状態。即時停止し、詳細点検が必要です。"
    
    if ae_status == 'alert':
        if fft_match:
            return 'alert', "特定の故障モードを伴う異常を検知。早期の部品交換を推奨します。"
        else:
            return 'warning', "原因不明の異常（AI検知）。センサーのガタや潤滑不良の可能性があります。"
            
    if fft_match and iso_zone == 'C':
        return 'warning', "物理的兆候が顕在化。傾向監視を強化してください。"
        
    if iso_zone in ['A', 'B'] and ae_status == 'normal':
        return 'normal', "設備状態は良好です。計画的な点検を継続してください。"
        
    return 'warning', "軽微な変動を検知。注意深く経過を観察してください。"

def generate_radar_chart(data_points, labels, output_path):
    """
    診断結果を可視化するレーダーチャートを生成
    """
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    data_points += data_points[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data_points, color='blue', alpha=0.25)
    ax.plot(angles, data_points, color='blue', linewidth=2)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # グリッド設定 (0: 正常, 1: 危険)
    ax.set_ylim(0, 1)
    plt.title("Integrated PdM Diagnosis Profile", size=15, color='blue', y=1.1)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    try:
        input_data = json.load(sys.stdin)
        inputs = input_data.get("inputs", {})
        metadata = input_data.get("metadata", {})
        
        equipment_id = metadata.get("equipment_id", "Unknown")
        
        # 各スキルからの情報抽出
        iso = inputs.get("iso_20816", {})
        fft = inputs.get("fft_spectrum", {})
        ae = inputs.get("autoencoder", {})
        lstm = inputs.get("lstm_trend", {})
        
        iso_zone = iso.get("zone", "A")
        ae_status = ae.get("status", "normal")
        
        # FFT整合性の簡易判定 (1X周波数付近にピークがあるか)
        fr = metadata.get("bearing_params", {}).get("fr", 0)
        peak_freqs = fft.get("peak_frequencies", [])
        fft_match = any(abs(p - fr) < 0.05 * fr for p in peak_freqs) if fr > 0 else False
        
        # 統合診断
        status, message = get_integrated_status(iso_zone, ae_status, fft_match)
        confidence = calculate_confidence(iso_zone, ae_status, fft_match)
        
        # レーダーチャート用データ算出 (0=Normal, 1=Danger)
        iso_val = {'A': 0.1, 'B': 0.3, 'C': 0.7, 'D': 1.0}.get(iso_zone, 0.1)
        ae_val = 1.0 if ae_status == 'alert' else 0.2
        fft_val = 0.8 if fft_match else 0.2
        lstm_val = max(0.0, 1.0 - (lstm.get("remaining_useful_life_days", 100) / 100.0))
        
        labels = ['ISO (RMS)', 'AI (Anomaly)', 'FFT (Pattern)', 'Trend (RUL)']
        vals = [iso_val, ae_val, fft_val, lstm_val]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{equipment_id}_integrated_{timestamp}.png"
        plot_rel_path = f"assets/plots/{plot_filename}"
        plot_abs_path = os.path.join(os.path.dirname(__file__), "..", "assets", "plots", plot_filename)
        
        generate_radar_chart(vals, labels, plot_abs_path)
        
        # 推奨アクション
        actions = {
            'alert': "直ちに運転を停止し、予備機への切り替えと軸受の交換を実施してください。",
            'warning': "次回の定期点検を前倒しし、潤滑状態の確認と増し締めを行ってください。",
            'normal': "現状の運転条件を維持し、次回の定期診断（3ヶ月後）を受けてください。"
        }
        
        next_date = (datetime.now() + timedelta(days=7 if status != 'normal' else 90)).strftime("%Y-%m-%d")
        
        output = {
            "status": status,
            "score": confidence,
            "method": "physics_informed_diagnosis",
            "features": {
                "overall_status": status.upper(),
                "confidence_score": confidence,
                "conflicting_indicators": ["ISO/AI Conflict"] if confidence < 0.5 else [],
                "recommended_action": actions.get(status, "経過観察"),
                "next_inspection_date": next_date,
                "plot_url": f".gemini/skills/physics_informed_diagnosis/{plot_rel_path}"
            },
            "message": message
        }
        
        print(json.dumps(output, indent=2, ensure_ascii=False))

    except Exception as e:
        error_res = {
            "status": "error",
            "error_code": "INTEGRATION_FAILED",
            "message": f"統合診断中にエラーが発生しました: {str(e)}",
            "suggestion": "入力JSONの形式が各スキルの標準スキーマに準拠しているか確認してください。"
        }
        print(json.dumps(error_res, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
