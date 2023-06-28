import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

# Wolrd map 
st.subheader("Wolrd map of devs")
fig3_01 = go.Figure(go.Scattergeo())
fig3_01.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple"
)
fig3_01.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig3_01.show()

# Interactive map
st.subheader("Interactive map of devs")
fig3_02 = go.Figure(go.Scattergeo())
fig3_02.update_geos(projection_type="orthographic")
fig3_02.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig3_02.show()
