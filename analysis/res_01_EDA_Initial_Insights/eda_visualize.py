import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

def visualize():
    df = pd.read_csv('processed_data/merged_train.csv')
    
    if not os.path.exists('reports/figures'):
        os.makedirs('reports/figures')
    
    # 1. Distribution of y
    fig1 = px.histogram(df, x='y', title='Distribution of Attendance (y)')
    fig1.write_html('reports/figures/dist_y.html')
    print("Attendance (y) stats:")
    print(df['y'].describe())
    
    # 2. y by stage
    fig2 = px.box(df, x='stage', y='y', title='Attendance by Stage (J1 vs J2)')
    fig2.write_html('reports/figures/y_by_stage.html')
    print("\nAttendance by Stage:")
    print(df.groupby('stage')['y'].describe())
    
    # 3. y vs capa
    fig3 = px.scatter(df, x='capa', y='y', color='stage', hover_data=['stadium'],
                      title='Attendance vs Stadium Capacity')
    fig3.write_html('reports/figures/y_vs_capa.html')
    
    # 4. y by day_of_week
    # 0=Mon, 5=Sat, 6=Sun
    fig4 = px.box(df, x='day_of_week', y='y', title='Attendance by Day of Week (0=Mon, 6=Sun)')
    fig4.write_html('reports/figures/y_by_dow.html')
    print("\nAttendance by Day of Week:")
    print(df.groupby('day_of_week')['y'].mean())

if __name__ == "__main__":
    visualize()
