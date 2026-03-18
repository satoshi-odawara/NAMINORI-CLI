import pandas as pd
import os

def preprocess_and_merge():
    # Load data
    train = pd.read_csv('inputdata/train.csv')
    condition = pd.read_csv('inputdata/condition.csv')
    stadium = pd.read_csv('inputdata/stadium.csv')
    
    # Merge train and condition on 'id'
    # 'condition' contains extra info for train matches
    df = pd.merge(train, condition, on='id', how='left')
    
    # Merge with stadium info on stadium name
    # In train.csv, column name is 'stadium'
    # In stadium.csv, column name is 'name'
    df = pd.merge(df, stadium, left_on='stadium', right_on='name', how='left')
    
    # Check for missing values after merge
    print("Missing values after merge:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    
    # Basic date processing
    # gameday format: 03/10(土) -> split by '('
    df['date'] = df['year'].astype(str) + '-' + df['gameday'].str.split('(').str[0]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m/%d')
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek # 0=Monday, 6=Sunday
    
    # Temperature and humidity
    # Humidity is object (e.g., '66%')
    df['humidity'] = df['humidity'].str.replace('%', '').astype(float)
    
    # --- Feature Engineering ---
    
    # 1. Weather Categorization
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
    
    df['weather_cat'] = df['weather'].apply(categorize_weather)
    
    # 2. Popular Team Flag
    # Top attendance/popular teams based on J-League knowledge
    popular_teams = ['浦和レッズ', '横浜Ｆ・マリノス', '鹿島アントラーズ', '名古屋グランパス', 'ガンバ大阪', '川崎フロンターレ', 'ＦＣ東京']
    df['is_popular'] = df.apply(lambda row: 1 if row['home'] in popular_teams or row['away'] in popular_teams else 0, axis=1)
    
    # 3. Derby Match Flag
    derby_pairs = [
        set(['浦和レッズ', '大宮アルディージャ']), # Saitama
        set(['ガンバ大阪', 'セレッソ大阪']),     # Osaka
        set(['ＦＣ東京', '川崎フロンターレ']),    # Tamagawa Clasico
        set(['清水エスパルス', 'ジュビロ磐田']),    # Shizuoka
        set(['横浜Ｆ・マリノス', '川崎フロンターレ']), # Kanagawa
        set(['横浜Ｆ・マリノス', '湘南ベルマーレ']),   # Kanagawa
        set(['川崎フロンターレ', '湘南ベルマーレ']),   # Kanagawa
        set(['横浜Ｆ・マリノス', '横浜ＦＣ']),       # Yokohama
    ]
    
    def check_derby(home, away):
        match_teams = set([home, away])
        for derby in derby_pairs:
            if derby.issubset(match_teams):
                return 1
        return 0
    
    df['is_derby'] = df.apply(lambda row: check_derby(row['home'], row['away']), axis=1)
    
    # 4. Handle Missing Values
    # In some datasets, there might be missing values in tv or referee
    # Fill with 'Unknown'
    df['referee'] = df['referee'].fillna('Unknown')
    
    # Save merged data
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')
    
    output_path = 'processed_data/merged_train.csv'
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data with features saved to {output_path}")
    print("Columns:", df.columns.tolist())

if __name__ == "__main__":
    preprocess_and_merge()
