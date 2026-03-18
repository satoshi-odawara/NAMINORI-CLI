import pandas as pd
import os
try:
    from analysis.res_02_Refined_Dataset.constants import POPULAR_TEAMS, DERBY_PAIRS, categorize_weather
except ImportError:
    from constants import POPULAR_TEAMS, DERBY_PAIRS, categorize_weather

def preprocess_and_merge():
    # Load data
    train = pd.read_csv('inputdata/train.csv')
    condition = pd.read_csv('inputdata/condition.csv')
    stadium = pd.read_csv('inputdata/stadium.csv')
    
    # Merge train and condition on 'id'
    df = pd.merge(train, condition, on='id', how='left')
    
    # Merge with stadium info on stadium name
    df = pd.merge(df, stadium, left_on='stadium', right_on='name', how='left')
    
    # Basic date processing
    df['date'] = df['year'].astype(str) + '-' + df['gameday'].str.split('(').str[0]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m/%d')
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek # 0=Monday, 6=Sunday
    
    # Temperature and humidity
    df['humidity'] = df['humidity'].str.replace('%', '').astype(float)
    
    # --- Feature Engineering ---
    
    # 1. Weather Categorization
    df['weather_cat'] = df['weather'].apply(categorize_weather)
    
    # 2. Popular Team Flag
    df['is_popular'] = df.apply(lambda row: 1 if row['home'] in POPULAR_TEAMS or row['away'] in POPULAR_TEAMS else 0, axis=1)
    
    # 3. Derby Match Flag
    def check_derby(home, away):
        match_teams = set([home, away])
        for derby in DERBY_PAIRS:
            if derby.issubset(match_teams):
                return 1
        return 0
    
    df['is_derby'] = df.apply(lambda row: check_derby(row['home'], row['away']), axis=1)
    
    # 4. Handle Missing Values
    df['referee'] = df['referee'].fillna('Unknown')
    
    # Save merged data
    output_path = 'analysis/res_02_Refined_Dataset/merged_train.csv'
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data with features saved to {output_path}")

if __name__ == "__main__":
    preprocess_and_merge()
