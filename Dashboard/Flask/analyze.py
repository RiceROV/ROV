import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
import tkinter as tk
from tkinter import filedialog
import os

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hides the main tkinter window
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")  # Opens dialog in the current working directory
    return file_path

def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')

def plot_combined_analysis_interactive(df, groups, titles):
    for columns, title in zip(groups, titles):
        fig = go.Figure()
        for column in columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Value',
            xaxis_rangeslider_visible=True
        )
        fig.show()


def plot_time_series_interactive(df, title='Overall Time Series Analysis'):
    fig = go.Figure()
    
    for column in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Value',
        xaxis_rangeslider_visible=True  # This makes the plot scrollable
    )
    
    fig.show()

def plot_specific_analysis_interactive(df, columns, title):
    fig = sp.make_subplots(rows=len(columns), cols=1, shared_xaxes=True, vertical_spacing=0.02)
    
    for i, column in enumerate(columns, start=1):
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column), row=i, col=1)

    fig.update_layout(
        title=title,
        height=300 * len(columns),  # Adjust the height based on the number of subplots
        xaxis_title='Time',
        showlegend=False
    )
    
    fig.show()

def plot_specific_analysis(df, columns, title):
    df[columns].plot(subplots=True, figsize=(10, 12))
    plt.title(title)
    plt.show()

def print_statistical_summary(df):
    print(df.describe())

def detect_and_plot_anomalies(df, columns, threshold=3):
    for col in columns:
        mean_val = df[col].mean()
        std_val = df[col].std()
        df[f'{col}_Z'] = (df[col] - mean_val) / std_val
        anomalies = df[np.abs(df[f'{col}_Z']) > threshold]
        
        plt.figure(figsize=(10, 2))
        plt.plot(df.index, df[col], label=col)
        plt.scatter(anomalies.index, anomalies[col], color='red', label='Anomalies')
        plt.title(f'Anomaly Detection in {col}')
        plt.legend()
        plt.show()

def perform_analysis():
    file_path = select_file()  # User selects the file through a dialog
    if not file_path:  # Check if the user has selected a file
        print("No file selected, exiting...")
        return
    
    df = load_data(file_path)
    
    plot_time_series_interactive(df, 'Detailed Time Series Analysis')
    plot_specific_analysis_interactive(df, ['Yaw', 'Roll', 'Pitch', 'Depth', 'Depth Set', 'Depth Control'], 'Yaw, Roll, Pitch, Depth Analysis')
    plot_specific_analysis_interactive(df, ['Thruster1', 'Thruster2', 'Thruster3', 'Thruster4', 'Thruster5', 'Thruster6'], 'Thrusters Performance Analysis')
    
    # Combined Analysis
    groups = [
        ['Thruster1', 'Thruster2', 'Thruster3', 'Thruster4', 'Thruster5', 'Thruster6'],
        ['BCD1', 'BCD2', 'BCD3', 'BCD4', 'BCD1 Volt', 'BCD2 Volt', 'BCD3 Volt', 'BCD4 Volt'],
        ['Yaw', 'Roll', 'Pitch', 'Depth', 'Depth Set', 'Depth Control', 'Thruster1', 'Thruster2', 'Thruster3', 'Thruster4', 'Thruster5', 'Thruster6', 'BCD1', 'BCD2', 'BCD3', 'BCD4', 'BCD1 Volt', 'BCD2 Volt', 'BCD3 Volt', 'BCD4 Volt']
    ]
    titles = [
        'Combined Thrusters Analysis',
        'Combined BCD and BCD Volt Analysis',
        'All Control Metrics Combined Analysis'
    ]
    
    plot_combined_analysis_interactive(df, groups, titles)

if __name__ == '__main__':
    perform_analysis()