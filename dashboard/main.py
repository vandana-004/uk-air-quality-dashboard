import dash
from dash import html, dcc
import pandas as pd
import sys
import os

# Load dataset from local path defined in config.py
try:
    from config import DATA_PATH
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows")
except FileNotFoundError:
    print("ERROR: CSV file not found. Check your DATA_PATH in config.py")
    df = None

app = dash.Dash(__name__)
app.title = "UK Air Quality Dashboard"

app.layout = html.Div([

    # ── Header
    html.Div([
        html.H1("UK Air Quality Dashboard"),
        html.P("Explore air pollution data across UK cities (2015–2023)")
    ], style={"textAlign": "center", "padding": "20px",
              "backgroundColor": "#1F4E79", "color": "white"}),

    # ── Error message if data not loaded
    html.Div(
        "Dataset not loaded. Please check DATA_PATH in config.py",
        style={"color": "red", "padding": "20px", "fontWeight": "bold"}
    ) if df is None else html.Div(),

    # ── City dropdown (shared across components)
    html.Div([
        html.Label("Select City:"),
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label": city, "value": city}
                     for city in sorted(df["site"].unique())] if df is not None else [],
            value=df["site"].unique()[0] if df is not None else None,
            clearable=False,
            style={"width": "400px"}
        )
    ], style={"padding": "20px"}),

    # ── Tabs
    dcc.Tabs([
        dcc.Tab(label="Pollution Trends", children=[
            html.Div(id="time-series-section",
                children=[html.P("Time series coming soon — Vandana (US10)")])
        ]),
        dcc.Tab(label="City Ranking", children=[
            html.Div(id="city-rank-section",
                children=[html.P("City ranking coming soon — Vandana (US11)")])
        ]),
        dcc.Tab(label="AQI Labels", children=[
            html.Div(id="aqi-section",
                children=[html.P("AQI labels coming soon — Nikhil (US9)")])
        ]),
        dcc.Tab(label="Summary Statistics", children=[
            html.Div(id="summary-stats-section",
                children=[html.P("Summary stats coming soon — Semih (US12)")])
        ]),
        dcc.Tab(label="Pollutant Info", children=[
            html.Div(id="pollutant-info-section",
                children=[html.P("Pollutant info coming soon — Semih (US13)")])
        ]),
    ], style={"padding": "20px"}),

])

if __name__ == "__main__":
    app.run(debug=True)
