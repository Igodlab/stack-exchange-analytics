# stack exchange stats go here
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

from cse.src.data_utils import *


# read data
data_load_state = st.progress(0, text="Reading data from cache...")
all_df, postsCsv = load_data(["ada", "eth", "sol"])
data_load_state = st.text("Done! (using cache)")

# grab initial and final date
t0 = postsCsv["ada"]["Date"].iloc[0]
tf = postsCsv["ada"]["Date"].iloc[-2]

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

