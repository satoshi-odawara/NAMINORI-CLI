import pandas as pd
import os

def load_and_inspect(file_path):
    print(f"--- Inspecting {file_path} ---")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    print("Shape:", df.shape)
    print("\nData Types and Missing Values:")
    print(df.info())
    print("\nSummary Statistics:")
    print(df.describe(include='all'))
    print("\nFirst 5 rows:")
    print(df.head())
    print("\n")
    return df

def main():
    train_df = load_and_inspect('inputdata/train.csv')
    condition_df = load_and_inspect('inputdata/condition.csv')
    stadium_df = load_and_inspect('inputdata/stadium.csv')

if __name__ == "__main__":
    main()
