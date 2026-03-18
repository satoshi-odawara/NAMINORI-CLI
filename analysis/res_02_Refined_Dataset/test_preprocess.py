import pandas as pd
import pytest
import os
from analysis.res_02_Refined_Dataset.preprocess import preprocess_and_merge

def test_preprocess_output_exists():
    # Ensure the script runs
    preprocess_and_merge()
    assert os.path.exists('analysis/res_02_Refined_Dataset/merged_train.csv')

def test_preprocess_features():
    df = pd.read_csv('analysis/res_02_Refined_Dataset/merged_train.csv')
    
    # Check if new columns exist
    assert 'weather_cat' in df.columns
    assert 'is_popular' in df.columns
    assert 'is_derby' in df.columns
    
    # Check weather_cat values
    expected_weather_cats = {'Sunny', 'Cloudy', 'Rainy', 'Indoor'}
    actual_weather_cats = set(df['weather_cat'].unique())
    assert actual_weather_cats.issubset(expected_weather_cats)
    
    # Check is_popular and is_derby are binary
    assert set(df['is_popular'].unique()).issubset({0, 1})
    assert set(df['is_derby'].unique()).issubset({0, 1})

def test_no_missing_values():
    df = pd.read_csv('analysis/res_02_Refined_Dataset/merged_train.csv')
    # Except 'referee' which we filled 'Unknown'
    # Actually, check if any null exists
    assert df.isnull().sum().sum() == 0
