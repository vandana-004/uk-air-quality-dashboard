pip install pandas plotly
import pandas as pd
import plotly.express as px

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("YOUR_FILE_PATH.csv")   # 🔁 replace with your file or link

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# -------------------------------
# SELECT POLLUTANT
# -------------------------------
pollutant = "pm25"   # ✅ correct column

# -------------------------------
# AQI + RECOMMENDATION
# -------------------------------
def calculate_aqi(pm25):
    if pm25 <= 12: return 50
    elif pm25 <= 35.4: return 100
    elif pm25 <= 55.4: return 150
    elif pm25 <= 150.4: return 200
    elif pm25 <= 250.4: return 300
    else: return 400

def get_recommendation(aqi):
    if aqi <= 50:
        return "Good air quality"
    elif aqi <= 100:
        return "Moderate – Sensitive people be careful"
    elif aqi <= 150:
        return "Unhealthy for sensitive groups"
    elif aqi <= 200:
        return "Unhealthy – Wear mask"
    elif aqi <= 300:
        return "Very Unhealthy – Stay indoors"
    else:
        return "Hazardous – Avoid going outside"

# -------------------------------
# CURRENT AQI
# -------------------------------
latest_pm25 = df["pm25"].dropna().iloc[-1]
aqi = calculate_aqi(latest_pm25)
rec = get_recommendation(aqi)

print(f"\nAQI: {aqi} | {rec}\n")

# -------------------------------
# TOP 5 POLLUTED LOCATIONS
# -------------------------------
top_sites = df.groupby("site")[pollutant].mean().reset_index()
top_sites = top_sites.sort_values(by=pollutant, ascending=False).head(5)

fig1 = px.bar(
    top_sites,
    x="site",
    y=pollutant,
    title="Top 5 Polluted Locations"
)
fig1.show()

# -------------------------------
# HOTSPOT MAP (FIXED)
# -------------------------------
map_data = df.groupby("site").mean(numeric_only=True).reset_index()

# ✅ FIX: remove NaN values (important)
map_data = map_data.dropna(subset=[pollutant, "latitude", "longitude"])

fig2 = px.scatter_map(
    map_data,
    lat="latitude",
    lon="longitude",
    color=pollutant,
    size=pollutant,
    hover_name="site",
    title="Pollution Hotspots"
)
fig2.show()

# -------------------------------
# HEATMAP (FIXED)
# -------------------------------
fig3 = px.density_map(
    map_data,
    lat="latitude",
    lon="longitude",
    z=pollutant,
    radius=15,
    center=dict(lat=55, lon=-3),
    zoom=4,
    title="Pollution Heatmap"
)
fig3.show()