import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from cse.src.data_utils import *

import os

#############################################################
# 
#    streamlit_app.py
#
#############################################################



# data path
# data_path = "./cse/data"

@st.cache_data
def load_data(nameList):
    assert nameList != None, "Please give at least one *.csv file name to be loaded"
    all_df = {}
    postsCsv = {}
    if type(nameList) is list:
        assert(len(nameList) >= 1), "List must not be empy"
        for n in nameList:
            csv_name = ""
            all_df[n] = load_csv("csv-out-"+n, fpath=os.path.join("cse", "data", n))
            postsCsv[n] = questionsAnalytics(all_df[n]["Posts"], freq=timedelta(days=7))

    elif type(nameList) is str:
        all_df[nameList] = load_csv("csv-out-"+nameList, fpath=os.path.join("cse", "data", nameList))
        postsCsv[nameList] = questionsAnalytics(all_df[nameList]["Posts"], freq=timedelta(days=7))

    return all_df, postsCsv

data_load_state = st.progress(0, text="Loading data...")
all_df, postsCsv = load_data(["ada", "eth", "sol"])
data_load_state = st.text("Done! (using cache)")

# grab initial and final date
t0 = postsCsv["ada"]["Date"].iloc[0]
tf = postsCsv["ada"]["Date"].iloc[-2]

# dashboard title
st.title("CSE metrics")

# define color tags
lineColor = {"ada": "deepskyblue",
             "eth": "purple",
             "dot": "pink",
             "sol": "black"}

ticker = {"ada": "ADA",
          "eth": "ETH",
          "dot": "DOT",
          "sol": "SOL"}

chainName = {"ada": "Cardano",
             "eth": "Ethereum",
             "dot": "Polkadot",
             "sol": "Solana"}

# Most popular tags figure 
st.subheader("Most discussed tags - bars")
(fig01, fig02) = postsTagsBarplot(all_df["ada"], startDate="2021-05", endDate="2022-06", nTags=10)
st.plotly_chart(fig02, use_container_width=True)


# Same as above as a pie-chart
st.subheader("Most discussed tags - piechart")
fig03 = postsTagsPieplot(all_df["ada"], startDate="2021-05", endDate="2022-06", nTags=12)
st.plotly_chart(fig03, use_container_width=True)

# for CSE cardano moderators
fig04 = make_subplots(rows=2, cols=1, 
                      shared_xaxes=True,
                      vertical_spacing=0.08,
                      subplot_titles=("# of questions per day", "% of questions answered")
                     )

for kk in all_df.keys():
    # number of questions per day
    fig04.add_trace(go.Scatter(
                             x=postsCsv[kk]["Date"], 
                             y=postsCsv[kk]["QuestionsDay"],
                             name=ticker[kk],
                             line_color=lineColor[kk],
                             legendgroup=ticker[kk],
                             mode="lines",
                             #showlegend=False
                             ),
                  row=1, col=1)
    
    # percentage of questions answered
    fig04.add_trace(go.Scatter(
                         x=postsCsv[kk]["Date"], 
                         y=postsCsv[kk]["PercQsAns"], 
                         #name="ans",
                         line_color=lineColor[kk],
                         legendgroup=ticker[kk],
                         mode="lines",
                         showlegend=False
                         ),
              row=2, col=1)
    
fig04.add_shape(type="line", x0=t0, y0=10, x1=tf, y1=10, line=dict(dash="dashdot"), row=1, col=1)
fig04.add_shape(type="line", x0=t0, y0=0.9, x1=tf, y1=0.9, line=dict(dash="dashdot"), row=2, col=1)


fig04.update_layout(font=dict(size=17), 
                    showlegend=True,
                    width=800,
                    height=1000,
                    )
#fig04.update_yaxes(type="log", row=1, col=1)
fig04.update_xaxes(range=[t0, tf], tickangle=45)
# fig04.show()


st.subheader("Daily stats, many chains comparisson")
st.plotly_chart(fig04, use_container_width=False)
# st.line_chart(postsCsv["ada"], 
#               x="Date",
#               y="QuestionsDay",
#               )

# fig04.write_image("../images/cse-ecosystem-comparisson.png") 
