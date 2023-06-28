# read data
import streamlit as st

from cse.src.data_utils import *

data_load_state = st.progress(0, text="Reading data from cache...")
all_df, postsCsv = load_data(["ada", "eth", "sol"])
data_load_state = st.text("Done! (using cache)")

# # Most popular tags figure 
st.subheader("Most discussed tags - bars")
(fig01, fig02) = postsTagsBarplot(all_df["ada"], startDate="2021-05", endDate="2022-06", nTags=10)
st.plotly_chart(fig02, use_container_width=True)


# Same as above as a pie-chart
st.subheader("Most discussed tags - piechart")
fig03 = postsTagsPieplot(all_df["ada"], startDate="2021-05", endDate="2022-06", nTags=12)
st.plotly_chart(fig03, use_container_width=True)

