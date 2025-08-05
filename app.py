
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import json

st.set_page_config(layout="wide", page_title="Resource Adequacy Visualization")

# Load data
draws_df = pd.read_csv("lole_draws.csv")
map_df = pd.read_csv("lole_map_data.csv")

with open("regions.geojson") as f:
    geojson_data = json.load(f)

# Style
PRIMARY_COLOR = "#007A33"
st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: #F7F9FB;
        }}
        .sidebar .sidebar-content {{
            background-color: white;
        }}
        h1, h2, h3, h4 {{
            color: {PRIMARY_COLOR};
        }}
        .stButton>button {{
            color: white;
            background-color: {PRIMARY_COLOR};
        }}
    </style>
""", unsafe_allow_html=True)

st.title("Resource Adequacy Visualization Tool")

# Draw selector
draw = st.slider("Select Monte Carlo Draw", min_value=1, max_value=50, value=1)

# Tabs
tab1, tab2 = st.tabs(["📊 Heatmaps", "🗺️ LOLE Risk Map"])

# --- Heatmaps ---
with tab1:
    st.subheader(f"LOLE Heatmaps – Change Case – Draw {draw}")
    regions = draws_df["Region"].unique()
    for region in sorted(regions):
        data = draws_df[
            (draws_df["Region"] == region) &
            (draws_df["Draw"] == draw) &
            (draws_df["Case"] == "Change Case")
        ].pivot(index="Month", columns="Hour", values="LOLE")

        st.markdown(f"**{region}**")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(data, cmap="YlOrRd", ax=ax, cbar_kws={'label': 'LOLE (days)'})
        st.pyplot(fig)

# --- Map View ---
with tab2:
    st.subheader(f"LOLE Risk Map – Draw {draw}")
    draw_map = map_df[map_df["Draw"] == draw]

    fig = px.choropleth_mapbox(
        draw_map,
        geojson=geojson_data,
        locations="Region",
        featureidkey="properties.Region",
        color="LOLE",
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 39.5, "lon": -98},
        opacity=0.7,
        labels={"LOLE": "Risk"},
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
