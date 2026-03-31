import os
import pandas as pd
import numpy as np
import json
from datetime import datetime

class IMSLoader:
    def __init__(self, fs=20480):
        """
        NASA IMS Dataset Loader
        fs: Sampling frequency (Default is 20,480 Hz)
        """
        self.fs = fs

    def parse_filename(self, filepath):
        """
        ファイル名から日時を抽出 (例: 2003.10.22.12.06.24)
        """
        filename = os.path.basename(filepath)
        try:
            return datetime.strptime(filename, "%Y.%m.%.d.%H.%M.%S")
        except:
            # 時折、秒数が含まれない、または形式が違う場合のフォールバック
            try:
                parts = filename.split('.')
                return datetime(int(parts[0]), int(parts[1]), int(parts[2]), 
                                int(parts[3]), int(parts[4]), int(parts[5]))
            except:
                return None

    def load_file(self, filepath, bearing_idx=0, test_type=1):
        """
        個別のデータファイルを読み込み、指定した軸受の信号を抽出する
        test_type 1: 1st test (8 bearings, 2 sensors per bearing = 16 columns)
        test_type 2: 2nd test (4 bearings, 1 sensor per bearing = 4 columns)
        """
        # IMSデータはタブまたはスペース区切り
        # 1st test は 16列 (B1x, B1y, B2x, B2y, ... B8x, B8y)
        # 2nd test は 4列 (B1, B2, B3, B4)
        
        try:
            # sep=None, engine='python' で自動的に区切り文字（タブ/スペース）を判別
            df = pd.read_csv(filepath, sep=r'\s+', header=None)
            
            if test_type == 1:
                # 1st test: 軸受iのデータは (i*2) と (i*2 + 1) 列目
                # ここでは代表して X軸 (i*2) を使用
                signal = df.iloc[:, bearing_idx * 2].values
            else:
                # 2nd/3rd test: 軸受iのデータは i 列目
                signal = df.iloc[:, bearing_idx].values
                
            timestamp = self.parse_filename(filepath)
            
            return {
                "signal": signal.tolist(),
                "fs": self.fs,
                "equipment_id": f"IMS_B{bearing_idx+1}_T{test_type}",
                "metadata": {
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "bearing_idx": bearing_idx,
                    "test_type": test_type,
                    "unit": "g", # IMSデータは重力加速度単位
                    "bearing_params": {
                        "fr": 33.33, # 2000 RPM / 60
                        "n": 16,     # ZA-2115 諸元
                        "d_D_ratio": 0.38
                    }
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def to_json(self, data, output_path=None):
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        return json.dumps(data)

if __name__ == "__main__":
    # テスト実行
    loader = IMSLoader()
    sample_path = "bench/IMS/1st_test/2003.10.22.12.06.24"
    if os.path.exists(sample_path):
        res = loader.load_file(sample_path, bearing_idx=0, test_type=1)
        print(f"Loaded signal length: {len(res['signal'])}")
        print(f"Timestamp: {res['metadata']['timestamp']}")
    else:
        print(f"File not found: {sample_path}")
