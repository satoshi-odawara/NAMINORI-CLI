# Domain Knowledge Constants

# Popular Teams based on J-League attendance records
POPULAR_TEAMS = [
    '浦和レッズ', 
    '横浜Ｆ・マリノス', 
    '鹿島アントラーズ', 
    '名古屋グランパス', 
    'ガンバ大阪', 
    '川崎フロンターレ', 
    'ＦＣ東京'
]

# Major Derby Match Pairs
DERBY_PAIRS = [
    set(['浦和レッズ', '大宮アルディージャ']),    # Saitama Derby
    set(['ガンバ大阪', 'セレッソ大阪']),        # Osaka Derby
    set(['ＦＣ東京', '川崎フロンターレ']),       # Tamagawa Clasico
    set(['清水エスパルス', 'ジュビロ磐田']),       # Shizuoka Derby
    set(['横浜Ｆ・マリノス', '川崎フロンターレ']),    # Kanagawa Derby
    set(['横浜Ｆ・マリノス', '湘南ベルマーレ']),      # Kanagawa Derby
    set(['川崎フロンターレ', '湘南ベルマーレ']),      # Kanagawa Derby
    set(['横浜Ｆ・マリノス', '横浜ＦＣ']),          # Yokohama Derby
]

# Weather Category Mapping Logic
def categorize_weather(w):
    if '雨' in w or '雪' in w or '雷' in w:
        return 'Rainy'
    elif '晴' in w:
        return 'Sunny'
    elif '曇' in w:
        return 'Cloudy'
    elif '屋内' in w:
        return 'Indoor'
    else:
        return 'Other'
