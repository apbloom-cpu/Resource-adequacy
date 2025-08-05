
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Resource Adequacy Visualizer")

PRIMARY_COLOR = "#007A33"
ACCENT_COLOR = "#00A9E0"
BACKGROUND_COLOR = "#F7F9FB"

st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {BACKGROUND_COLOR};
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

df = pd.read_csv("lole_data.csv")

region = st.sidebar.selectbox("Select Region", sorted(df["Region"].unique()))
case = st.sidebar.radio("Select Case", ["Base Case", "Change Case"])

filtered = df[(df["Region"] == region) & (df["Case"] == case)].drop(columns=["Region", "Case"])
months = filtered["Month"]
heatmap_data = filtered.drop(columns=["Month"]).to_numpy()

st.subheader(f"{region} – {case}")
fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", xticklabels=filtered.columns[1:], yticklabels=months, ax=ax, cbar_kws={'label': 'LOLE (days)'})
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Month")
ax.set_title("LOLE Heatmap by Hour and Month")
st.pyplot(fig)

st.subheader("Risk Duration Curve")
threshold = 0.1
draws = 50
hours = 24
months = 12
values = []

for i in range(draws):
    simulated = heatmap_data + 0.01 * np.random.randn(*heatmap_data.shape)
    values.append((simulated > threshold).sum())

values.sort(reverse=True)
plt.figure(figsize=(10, 4))
plt.plot(values, color=PRIMARY_COLOR)
plt.xlabel("Draw Number (Sorted)")
plt.ylabel("Hours > 0.1 LOLE")
plt.title("Risk Duration Curve")
st.pyplot(plt)

st.info("Stacked resource sufficiency timeline coming soon.")
