map_data = (
    df.groupby("site")
    .agg({
        "latitude": "first",
        "longitude": "first",
        pollutant: "mean"
    })
    .reset_index()
)

map_data = map_data.dropna(subset=[pollutant, "latitude", "longitude"])

map_fig = px.scatter_mapbox(
    map_data,
    lat="latitude",
    lon="longitude",
    color=pollutant,
    size=pollutant,
    hover_name="site",
    color_continuous_scale="Reds",
    zoom=4,
    height=500,
    title=f"Pollution Hotspots based on {pollutant.upper()}"
)
map_fig.update_layout(mapbox_style="open-street-map")
