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
    # humidity is object (e.g., '66%')
    df['humidity'] = df['humidity'].str.replace('%', '').astype(float)
    
    # Save merged data
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')
    
    output_path = 'processed_data/merged_train.csv'
    df.to_csv(output_path, index=False)
    print(f"Merged data saved to {output_path}")
    print("Columns:", df.columns.tolist())

if __name__ == "__main__":
    preprocess_and_merge()
