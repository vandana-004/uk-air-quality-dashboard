from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import DATA_PATH

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date", "site"])

df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Season mapping (User Story 3)
def get_season(month):
    if month in [12,1,2]:
        return "Winter"
    elif month in [3,4,5]:
        return "Spring"
    elif month in [6,7,8]:
        return "Summer"
    else:
        return "Autumn"

df["season"] = df["month"].apply(get_season)

pollutants = ["co", "nox", "no2", "o3", "so2", "pm10", "pm2.5"]

# KPI values
avg_pm25 = round(df["pm2.5"].mean(), 2)
avg_no2 = round(df["no2"].mean(), 2)
avg_o3 = round(df["o3"].mean(), 2)

# -------------------------------
# DASH APP
# -------------------------------
app = Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H1("Sprint 4 - Air Quality Insights",
            style={"textAlign":"center"}),

    # Filters
    html.Div([
        html.Label("Select Pollutant"),
        dcc.Dropdown(
            id="pollutant",
            options=[{"label":i.upper(),"value":i} for i in pollutants],
            value="pm2.5"
        ),

        html.Br(),

        html.Label("Select City"),
        dcc.Dropdown(
            id="city",
            options=[{"label":i,"value":i} for i in df["site"].dropna().unique()],
            value=df["site"].dropna().unique()[0]
        )

    ], style={"width":"30%","margin":"auto"}),

    html.Br(),

    html.H1(
        "UK Air Quality Analytics Dashboard",
        style={"textAlign": "center", "marginBottom": "30px"}
    ),

    html.Button("Download Cleaned Dataset", id="download-btn"),
    dcc.Download(id="download-data"),

    html.Br(),
    html.Br(),

    html.Label("Select Date Range"),
    dcc.DatePickerRange(
        id="date-range",
        start_date=df["date"].min().date(),
        end_date=df["date"].max().date()
    ),

    html.Br(),
    html.Br(),

    # KPI Cards
    html.Div([
        html.Div([html.H4("Average PM2.5"), html.H2(avg_pm25)], className="card"),
        html.Div([html.H4("Average NO2"), html.H2(avg_no2)], className="card"),
        html.Div([html.H4("Average O3"), html.H2(avg_o3)], className="card"),
    ], style={"display": "flex", "justifyContent": "space-around"}),

    html.Br(),

    # Filters
    html.Div([
        html.Label("Select Monitoring Site"),
        dcc.Dropdown(
            id="site",
            options=[{"label": i, "value": i} for i in sorted(df["site"].dropna().unique())],
            value=sorted(df["site"].dropna().unique())[0]
        ),

        html.Br(),

        html.Label("Select Pollutant"),
        dcc.Dropdown(
            id="pollutant",
            options=[{"label": i.upper(), "value": i} for i in pollutants],
            value="pm2.5"
        )
    ], style={"width": "30%", "margin": "auto"}),

    html.Br(),

    html.Div(id="stats-box"),
    html.Br(),
    html.Div(id="pollutant-info"),
    html.Br(),

    # Graphs
    html.Div([
        dcc.Graph(id="trend_graph"),
        dcc.Graph(id="monthly_graph")
    ]),

    html.Div([
        dcc.Graph(id="site_graph"),
        dcc.Graph(id="distribution_graph")
    ]),

    dcc.Graph(id="bubble-chart"),
    dcc.Graph(id="correlation_graph"),
    dcc.Graph(id="map_graph"),

    # -------------------------------
    # USER STORY 18
    # -------------------------------
    html.H2("Advanced Insights"),
    html.Div(id="most_polluted_year"),
    dcc.Graph(id="year_graph"),

    # -------------------------------
    # USER STORY 19
    # -------------------------------
    html.Div(id="most_polluted_month"),
    dcc.Graph(id="month_graph"),

    # -------------------------------
    # USER STORY 20
    # -------------------------------
    html.Div(id="best_season"),
    dcc.Graph(id="season_graph")
])


# -------------------------------
# DOWNLOAD CALLBACK
# -------------------------------
@app.callback(
    Output("download-data", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_dataset(n_clicks):
    return dcc.send_data_frame(df.to_csv, "UK_Air_Quality_Cleaned.csv", index=False)

# -------------------------------
# DASHBOARD CALLBACK
# -------------------------------
@app.callback(
    Output("trend_graph", "figure"),
    Output("monthly_graph", "figure"),
    Output("site_graph", "figure"),
    Output("distribution_graph", "figure"),
    Output("bubble-chart", "figure"),
    Output("correlation_graph", "figure"),
    Output("map_graph", "figure"),
    Output("stats-box", "children"),
    Output("pollutant-info", "children"),
    Output("most_polluted_year", "children"),
    Output("year_graph", "figure"),
    Output("most_polluted_month", "children"),
    Output("month_graph", "figure"),
    Output("best_season", "children"),
    Output("season_graph", "figure"),
    Input("pollutant", "value"),
    Input("city", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_dashboard(pollutant, city, start_date, end_date):

    filtered = df[
        (df["site"] == city) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ].copy()

    filtered = filtered.dropna(subset=[pollutant])

    if filtered.empty:
        empty_fig = {}
        no_stats = html.Div("No data available for the selected filters.")
        no_info = html.Div("No description available.")
        no_text = html.Div("No result available.")
        return (
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            no_stats,
            no_info,
            no_text,
            empty_fig,
            no_text,
            empty_fig,
            no_text,
            empty_fig
        )

    filtered = filtered.sort_values("date").tail(1000)

    stats_box = html.Div([
        html.H4(f"{pollutant.upper()} Summary Statistics"),
        html.P(f"Mean: {filtered[pollutant].mean():.2f}"),
        html.P(f"Minimum: {filtered[pollutant].min():.2f}"),
        html.P(f"Maximum: {filtered[pollutant].max():.2f}"),
        html.P(f"Standard Deviation: {filtered[pollutant].std():.2f}")
    ])

    # -------------------------------
    # USER STORY 18: Most Polluted Year
    # -------------------------------
    
    year_avg = df.groupby("year")[pollutant].mean().reset_index()
    worst_year = year_avg.sort_values(by=pollutant, ascending=False).iloc[0]["year"]

    year_fig = px.bar(
        year_avg,
        x="year",
        y=pollutant,
        title="Average Pollution by Year"
    )

    year_text = html.H2(
        f"Most Polluted Year: {int(worst_year)}",
        style={"textAlign":"center","color":"red"}
    )

    # -------------------------------
    # USER STORY 19: Most Polluted Month
    # -------------------------------
    month_avg = df.groupby("month")[pollutant].mean().reset_index()
    worst_month = month_avg.sort_values(by=pollutant, ascending=False).iloc[0]["month"]

    month_fig = px.bar(
        month_avg,
        x="month",
        y=pollutant,
        title="Average Pollution by Month"
    )

    month_text = html.H2(
        f"Most Polluted Month: {int(worst_month)}",
        style={"textAlign":"center","color":"red"}
    )

    # -------------------------------
    # USER STORY 20: Best Season (City Based)
    # -------------------------------
    city_df = df[df["site"] == city]

    season_avg = city_df.groupby("season")[pollutant].mean().reset_index()
    best_season_val = season_avg.sort_values(by=pollutant, ascending=True).iloc[0]["season"]

    season_fig = px.bar(
        season_avg,
        x="season",
        y=pollutant,
        title=f"Seasonal Air Quality in {city}"
    )

    season_text = html.H2(
        f"Best Season to Visit {city}: {best_season_val}",
        style={"textAlign":"center","color":"green"}
    )

    pollutant_descriptions = {
        "no2": "Nitrogen dioxide is mainly produced by road traffic and can irritate the lungs.",
        "pm2.5": "PM2.5 refers to very small particles that can enter deep into the lungs and bloodstream.",
        "co": "Carbon monoxide is a poisonous gas formed by incomplete combustion.",
        "o3": "Ground-level ozone is a harmful air pollutant that can affect breathing.",
        "pm10": "PM10 includes inhalable particles that may affect the respiratory system.",
        "so2": "Sulphur dioxide can irritate the nose, throat, and lungs.",
        "nox": "Nitrogen oxides are gases mainly produced during fuel combustion."
    }

    pollutant_info = html.Div([
        html.H4(f"About {pollutant.upper()}"),
        html.P(pollutant_descriptions.get(pollutant, "No description available."))
    ])

    trend = px.line(
        filtered,
        x="date",
        y=pollutant,
        title=f"{pollutant.upper()} Trend",
        color_discrete_sequence=["#00CC96"]
    )

    monthly = filtered.groupby("month")[pollutant].mean().reset_index()
    monthly_fig = px.bar(
        monthly,
        x="month",
        y=pollutant,
        color=pollutant,
        color_continuous_scale="Reds",
        title="Monthly Average"
    )

    site_avg = df.groupby("site")[pollutant].mean().reset_index().head(20)
    site_avg["highlight"] = site_avg[pollutant].apply(
        lambda x: "Worst Site" if x == site_avg[pollutant].max() else "Other Sites"
    )

    site_fig = px.bar(
        site_avg,
        y="site",
        x=pollutant,
        color="highlight",
        orientation="h",
        title="Average Pollutant by Site"
    )

    dist = px.histogram(
        filtered,
        x=pollutant,
        nbins=40,
        title="Distribution",
        color_discrete_sequence=["#636EFA"]
    )

    bubble_fig = px.scatter(
        filtered,
        x="pm2.5",
        y="no2",
        size="co",
        color="o3",
        hover_name="site",
        title="Pollution Relationship: PM2.5 vs NO2, CO, and O3"
    )

    corr = df[pollutants].dropna().sample(min(5000, len(df.dropna(subset=pollutants)))).corr()
    corr_fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )

    map_data = df.groupby("site").first().reset_index()

    map_fig = px.scatter_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        hover_name="site",
        zoom=4,
        height=500,
        color="site"
    )
    map_fig.update_layout(mapbox_style="open-street-map")

    

    return (
        trend,
        monthly_fig,
        site_fig,
        dist,
        bubble_fig,
        corr_fig,
        map_fig,
        stats_box,
        pollutant_info,
        year_text, 
        year_fig, 
        month_text, 
        month_fig, 
        season_text, 
        season_fig
    )

if __name__ == "__main__":
    app.run(debug=True)
